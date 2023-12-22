# Copyright (c) 2023 Michael Hu.
# This code is part of the book "The Art of Reinforcement Learning: Fundamentals, Mathematics, and Implementation with Python.".
# See the accompanying LICENSE file for details.


import collections
from typing import Tuple
import os

from absl import app
from absl import flags
import logging
import math

import torch
from torch import nn
from torch.distributions import Categorical

import numpy as np


import trackers as trackers_lib
import csv_writer
import gym_env_processor


FLAGS = flags.FLAGS
flags.DEFINE_string(
    'environment_name',
    'Pong',
    'Atari name without NoFrameskip and version, like Breakout, Pong, Seaquest.',
)
flags.DEFINE_integer('environment_height', 84, 'Environment frame screen height.')
flags.DEFINE_integer('environment_width', 84, 'Environment frame screen width.')
flags.DEFINE_integer('environment_frame_skip', 4, 'Skip frames by number of action repeats.')
flags.DEFINE_integer('environment_frame_stack', 4, 'Number of frames to stack.')
flags.DEFINE_bool('clip_grad', True, 'Clip gradients, default on.')
flags.DEFINE_float('max_grad_norm', 5.0, 'Max gradients norm when do gradients clip.')
flags.DEFINE_integer('batch_size', 64, 'Sample batch size when updating the neural network.')
flags.DEFINE_float('learning_rate', 0.00025, 'Learning rate for policy network.')
flags.DEFINE_float('discount', 0.99, 'Discount rate.')
flags.DEFINE_float('entropy_coef', 0.025, 'Coefficient for the entropy loss.')
flags.DEFINE_float('value_coef', 0.5, 'Coefficient for the state-value loss.')
flags.DEFINE_integer('sequence_length', 128, 'Collect N transitions before update parameters.')

flags.DEFINE_integer('num_iterations', 100, 'Number iterations to run.')
flags.DEFINE_integer(
    'num_train_steps',
    int(1e6 / 4),
    'Number training environment steps or frames (after frame skip) to run per iteration.',
)
flags.DEFINE_integer(
    'num_eval_steps',
    int(2e5),
    'Number evaluation environment steps or frames (after frame skip) to run per iteration.',
)

flags.DEFINE_integer('seed', 1, 'Runtime seed.')
flags.DEFINE_string(
    'checkpoint_dir',
    '',
    'Directory to store checkpoint file, default empty means do not create checkpoint.',
)
flags.DEFINE_string('results_csv_path', '', 'Path for CSV log file.')


def calc_conv2d_output(h_w, kernel_size: int = 1, stride: int = 1, pad: int = 0, dilation: int = 1):
    """Takes a tuple of (h,w) and returns a tuple of (h,w)"""

    if not isinstance(kernel_size, Tuple):
        kernel_size = (kernel_size, kernel_size)

    h = math.floor(((h_w[0] + (2 * pad) - (dilation * (kernel_size[0] - 1)) - 1) / stride) + 1)
    w = math.floor(((h_w[1] + (2 * pad) - (dilation * (kernel_size[1] - 1)) - 1) / stride) + 1)
    return (h, w)


def initialize_weights(net: nn.Module) -> None:
    """Initialize weights for Conv2d and Linear layers using kaming initializer."""
    assert isinstance(net, nn.Module)

    for module in net.modules():
        if isinstance(module, (nn.Conv2d, nn.Linear)):
            nn.init.kaiming_normal_(module.weight, nonlinearity='relu')

            if module.bias is not None:
                nn.init.zeros_(module.bias)


class ActorCriticConvNet(nn.Module):
    """Conv2d policy network with baseline head."""

    def __init__(self, state_dim: int, action_dim: int):
        """
        Args:
            state_dim: the dimension of the input vector to the neural network
            action_dim: the number of units for the output liner layer
        """
        super().__init__()

        # Compute the output shape of final conv2d layer
        c, h, w = state_dim
        h, w = calc_conv2d_output((h, w), 8, 4)
        h, w = calc_conv2d_output((h, w), 4, 2)
        h, w = calc_conv2d_output((h, w), 3, 1)
        conv2d_out_size = 64 * h * w

        self.body = nn.Sequential(
            nn.Conv2d(in_channels=c, out_channels=32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(conv2d_out_size, 512),
            nn.ReLU(),
        )

        self.policy_head = nn.Linear(512, action_dim)

        self.value_head = nn.Linear(512, 1)

        initialize_weights(self)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Given state, returns raw probabilities logits for all possible actions
        and the predicted state value."""
        x = x.float() / 255.0
        features = self.body(x)

        # Predict action distributions wrt policy
        pi_logits = self.policy_head(features)

        # Predict state-value
        value = self.value_head(features)
        return pi_logits, value


class ActorCriticAgent:
    """Actor-Critic agent for interacting with the environment and do learning."""

    def __init__(
        self,
        policy_network,
        policy_optimizer,
        discount,
        value_coef,
        entropy_coef,
        sequence_length,
        device,
    ):
        self.device = device

        self.policy_network = policy_network.to(device=self.device)
        self.policy_optimizer = policy_optimizer
        self.discount = discount
        self.value_coef = value_coef
        self.entropy_coef = entropy_coef

        self.sequence_length = sequence_length
        self.sequence = []

        # Counters and statistics
        self.step_t = -1
        self.update_t = 0

    def act(self, observation, reward, done):
        """Given an environment observation, returns an action.
        Also (conditionally) update network parameters."""
        self.step_t += 1

        a_t, v_t = self.choose_action(observation)

        self.sequence.append((observation, a_t, v_t, reward, done))

        if len(self.sequence) >= self.sequence_length:
            self.update()

            del self.sequence[:]

        return a_t

    def update(self):
        self.policy_optimizer.zero_grad()

        transitions = self.get_transitions_from_sequence(self.sequence)

        # Unpack list of tuples into separate lists
        s_t, a_t, return_t, advantage_t = map(list, zip(*transitions))

        s_t = torch.from_numpy(np.stack(s_t, axis=0)).to(device=self.device, dtype=torch.float32)
        a_t = torch.from_numpy(np.stack(a_t, axis=0)).to(device=self.device, dtype=torch.int64)  # Actions are discrete
        return_t = torch.from_numpy(np.stack(return_t, axis=0)).to(device=self.device, dtype=torch.float32)
        advantage_t = torch.from_numpy(np.stack(advantage_t, axis=0)).to(device=self.device, dtype=torch.float32)

        # Given past states, get predicted action probabilities and state value
        pi_logits_t, v_t = self.policy_network(s_t)
        pi_m = Categorical(logits=pi_logits_t)
        pi_logprob_a_t = pi_m.log_prob(a_t)
        entropy_loss = pi_m.entropy()

        policy_loss = advantage_t.detach() * pi_logprob_a_t

        value_loss = 0.5 * torch.square(return_t - v_t.squeeze(-1))

        # Averaging over batch dimension
        policy_loss = torch.mean(policy_loss)
        entropy_loss = torch.mean(entropy_loss)
        value_loss = torch.mean(value_loss)

        # Negative sign to indicate we want to maximize the policy gradient objective function
        loss = -(policy_loss + self.entropy_coef * entropy_loss) + self.value_coef * value_loss

        # Compute gradients
        loss.backward()

        # Update parameters
        self.policy_optimizer.step()

        self.update_t += 1

    def get_transitions_from_sequence(self, sequence):
        # Unpack list of tuples into separate lists.
        (observations, actions, values, rewards, dones) = map(list, zip(*sequence))

        # Our transitions in self.sequence is actually mismatched.
        # For example, the reward is one step behind, and there's not successor states
        # so we need to offset this
        s_t = observations[:-1]
        a_t = actions[:-1]
        v_t = values[:-1]
        r_t = rewards[1:]

        v_tp1 = values[1:]
        done_tp1 = dones[1:]

        # Compute returns and advantages
        return_t, advantage_t = self.compute_returns_and_advantages(v_t, r_t, v_tp1, done_tp1)

        # Zip multiple lists into list of tuples
        transitions = list(zip(s_t, a_t, return_t, advantage_t))

        return transitions

    def compute_returns_and_advantages(self, v_t, r_t, v_tp1, done_tp1):
        v_t = np.stack(v_t, axis=0)
        r_t = np.stack(r_t, axis=0)
        v_tp1 = np.stack(v_tp1, axis=0)
        done_tp1 = np.stack(done_tp1, axis=0)

        discount_tp1 = (~done_tp1).astype(np.float32) * self.discount

        # Finite horizon returns
        delta_t = r_t + discount_tp1 * v_tp1 - v_t
        advantage_t = np.zeros_like(delta_t, dtype=np.float32)

        g_t = 0
        for i in reversed(range(len(delta_t))):
            g_t = delta_t[i] + discount_tp1[i] * g_t
            advantage_t[i] = g_t

        return_t = advantage_t + v_t
        advantage_t = (advantage_t - advantage_t.mean()) / (advantage_t.std() + 1e-8)

        return return_t, advantage_t

    @torch.no_grad()
    def choose_action(self, observation):
        """Given an environment observation, returns an action according to the policy."""
        s_t = torch.from_numpy(observation[None, ...]).to(device=self.device, dtype=torch.float32)
        pi_logits, value = self.policy_network(s_t)
        pi_m = Categorical(logits=pi_logits)
        a_t = pi_m.sample()

        return a_t.squeeze(0).cpu().item(), value.squeeze(0).cpu().item()


class PolicyGreedyActor:
    """Policy greedy actor for evaluation only."""

    def __init__(self, policy_network, device):
        self.device = device
        self.policy_network = policy_network.to(device=device)

    def act(self, observation):
        """Given an environment observation, returns an action."""
        return self.choose_action(observation)

    @torch.no_grad()
    def choose_action(self, observation):
        """Given an environment observation, returns an action according to the policy."""
        s_t = torch.tensor(observation[None, ...]).to(device=self.device, dtype=torch.float32)
        pi_logits, _ = self.policy_network(s_t)
        pi_probs = torch.softmax(pi_logits, dim=-1)
        a_t = torch.argmax(pi_probs, dim=-1)
        return a_t.cpu().item()


def run_train_loop(env, agent, num_train_steps):
    """Run training for some steps."""
    trackers = trackers_lib.make_default_trackers()

    t = 0

    while t < num_train_steps:
        s_t = env.reset()
        r_t = 0
        done = False

        while True:
            a_t = agent.act(s_t, r_t, done)

            # Take the action in the environment and observe successor state and reward.
            s_t, r_t, done, info = env.step(a_t)

            t += 1

            # Only keep track of non-clipped/unscaled raw reward when collecting statistics
            raw_reward = r_t
            if 'raw_reward' in info and isinstance(info['raw_reward'], (float, int)):
                raw_reward = info['raw_reward']

            for tracker in trackers:
                tracker.step(raw_reward, done)

            if done:
                # Send the final transition to the agent before reset
                unsued_a_t = agent.act(s_t, r_t, done)  # noqa: F841
                break

    return trackers_lib.generate_statistics(trackers)


def run_evaluation_loop(env, agent, num_eval_steps):
    """Run evaluation for some steps."""
    trackers = trackers_lib.make_default_trackers()

    s_t = env.reset()
    for _ in range(num_eval_steps):
        a_t = agent.act(s_t)
        s_t, r_t, done, _ = env.step(a_t)

        for tracker in trackers:
            tracker.step(r_t, done)

        if done:
            s_t = env.reset()

    return trackers_lib.generate_statistics(trackers)


def main(argv):
    """Trains Actor-Critic agent.

    For every iteration, the code does these in sequence:
        1. Run agent for num_train_steps and periodically update network parameters
        2. Run evaluation agent for num_eval_steps with a separate evaluation environment
        3. Logging statistics to a csv file
        4. Create checkpoint file

    """
    del argv

    random_state = np.random.RandomState(FLAGS.seed)
    torch.manual_seed(FLAGS.seed)
    if torch.backends.cudnn.enabled:
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    logging.info(f'Runs Actor-Critic agent on {device}')

    writer = None
    if FLAGS.results_csv_path:
        writer = csv_writer.CsvWriter(FLAGS.results_csv_path)

    def environment_builder():
        return gym_env_processor.create_atari_environment(
            env_name=FLAGS.environment_name,
            frame_height=FLAGS.environment_height,
            frame_width=FLAGS.environment_width,
            frame_skip=FLAGS.environment_frame_skip,
            frame_stack=FLAGS.environment_frame_stack,
            seed=random_state.randint(1, 2**10),
            terminal_on_life_loss=True,
        )

    # Create training and evaluation environments
    train_env = environment_builder()
    eval_env = environment_builder()

    action_dim = train_env.action_space.n
    state_dim = train_env.observation_space.shape

    logging.info('Environment: %s', train_env.spec.id)
    logging.info('Action space: %s', action_dim)
    logging.info('Observation space: %s', state_dim)

    # Initialize network and optimizer
    policy_network = ActorCriticConvNet(state_dim=state_dim, action_dim=action_dim)
    policy_optimizer = torch.optim.Adam(policy_network.parameters(), lr=FLAGS.learning_rate)

    # Create training and evaluation agent instances
    train_agent = ActorCriticAgent(
        policy_network=policy_network,
        policy_optimizer=policy_optimizer,
        discount=FLAGS.discount,
        value_coef=FLAGS.value_coef,
        entropy_coef=FLAGS.entropy_coef,
        sequence_length=FLAGS.sequence_length,
        device=device,
    )

    eval_agent = PolicyGreedyActor(
        policy_network=policy_network,
        device=device,
    )

    # Start to run training and evaluation iterations
    for iteration in range(1, FLAGS.num_iterations + 1):
        # Run training steps
        policy_network.train()
        train_stats = run_train_loop(train_env, train_agent, FLAGS.num_train_steps)

        # Run evaluation steps
        policy_network.eval()
        eval_stats = run_evaluation_loop(eval_env, eval_agent, FLAGS.num_eval_steps)

        # Logging
        log_output = [
            ('iteration', iteration, '%3d'),
            ('step', iteration * FLAGS.num_train_steps * FLAGS.environment_frame_skip, '%5d'),
            ('train_step_rate', train_stats['step_rate'], '% 2.2f'),
            ('train_episode_return', train_stats['mean_episode_return'], '% 2.2f'),
            ('train_num_episodes', train_stats['num_episodes'], '%3d'),
            ('eval_episode_return', eval_stats['mean_episode_return'], '% 2.2f'),
            ('eval_num_episodes', eval_stats['num_episodes'], '%3d'),
        ]
        log_output_str = ', '.join(('%s: ' + f) % (n, v) for n, v, f in log_output)
        logging.info(log_output_str)

        if writer:
            writer.write(collections.OrderedDict((n, v) for n, v, _ in log_output))

        # Create checkpoint files
        if FLAGS.checkpoint_dir and os.path.exists(FLAGS.checkpoint_dir):
            torch.save(
                {
                    'policy_network': policy_network.state_dict(),
                },
                os.path.join(FLAGS.checkpoint_dir, f'{FLAGS.environment_name}_iteration_{iteration}.ckpt'),
            )

    if writer:
        writer.close()


if __name__ == '__main__':
    app.run(main)
