# Copyright (c) 2023 Michael Hu.
# This code is part of the book "The Art of Reinforcement Learning: Fundamentals, Mathematics, and Implementation with Python.".
# See the accompanying LICENSE file for details.


"""Trackers to collect statistics during training or evaluation."""

import collections
from pathlib import Path
import timeit
import numpy as np

from torch.utils.tensorboard import SummaryWriter


def _is_dict(_info):
    return _info is not None and isinstance(_info, dict)


class EpisodeTracker:
    """Tracks episode return and other statistics."""

    def __init__(self):
        self._num_steps_since_reset = None
        self._episode_returns = None
        self._episode_steps = None
        self._episode_visited_rooms = None
        self._current_episode_rewards = None
        self._current_episode_step = None

    def step(self, reward, done, info) -> None:
        """Accumulates statistics from timestep."""
        self._current_episode_rewards.append(reward)

        self._num_steps_since_reset += 1
        self._current_episode_step += 1

        if done:
            if _is_dict(info) and 'episode_visited_rooms' in info:
                self._episode_visited_rooms.append(info['episode_visited_rooms'])

            self._episode_returns.append(sum(self._current_episode_rewards))
            self._episode_steps.append(self._current_episode_step)
            self._current_episode_rewards = []
            self._current_episode_step = 0

    def reset(self) -> None:
        """Resets all gathered statistics, not to be called between episodes."""
        self._num_steps_since_reset = 0
        self._episode_returns = []
        self._episode_steps = []
        self._episode_visited_rooms = []
        self._current_episode_step = 0
        self._current_episode_rewards = []

    def get(self):
        """Aggregates statistics and returns as a dictionary.
        Here the convention is `episode_return` is set to `current_episode_return`
        if a full episode has not been encountered. Otherwise it is set to
        `mean_episode_return` which is the mean return of complete episodes only. If
        no steps have been taken at all, `episode_return` is set to `NaN`.
        Returns:
          A dictionary of aggregated statistics.
        """
        if len(self._episode_returns) > 0:
            mean_episode_return = np.array(self._episode_returns).mean()
            mean_episode_visited_rooms = np.array(self._episode_visited_rooms).mean()
        else:
            if self._num_steps_since_reset > 0:
                current_episode_return = sum(self._current_episode_rewards)
            else:
                current_episode_return = np.nan
            mean_episode_return = current_episode_return
            mean_episode_visited_rooms = 0

        return {
            'mean_episode_return': mean_episode_return,
            'mean_episode_visited_rooms': mean_episode_visited_rooms,
            'num_episodes': len(self._episode_returns),
            'current_episode_step': self._current_episode_step,
            'num_steps_since_reset': self._num_steps_since_reset,
        }


class StepRateTracker:
    """Tracks step rate, number of steps taken and duration since last reset."""

    def __init__(self):
        self._num_steps_since_reset = None
        self._start = None

    def step(self, reward, done, info) -> None:
        del (reward, done)
        self._num_steps_since_reset += 1

    def reset(self) -> None:
        self._num_steps_since_reset = 0
        self._start = timeit.default_timer()

    def get(self):
        duration = timeit.default_timer() - self._start
        if self._num_steps_since_reset > 0:
            step_rate = self._num_steps_since_reset / duration
        else:
            step_rate = np.nan
        return {
            'step_rate': step_rate,
            'num_steps': self._num_steps_since_reset,
            'duration': duration,
        }


class TensorboardEpisodeTracker(EpisodeTracker):
    """Extend EpisodeTracker to write to tensorboard"""

    def __init__(self, writer: SummaryWriter):
        super().__init__()
        self._total_steps = 0  # keep track total number of steps, does not reset
        self._total_episodes = 0  # keep track total number of episodes, does not reset
        self._writer = writer

    def step(self, reward, done, info) -> None:
        super().step(reward, done, info)

        self._total_steps += 1

        # To improve performance, only logging at end of an episode.
        if done:
            self._total_episodes += 1
            tb_steps = self._total_steps

            # tracker per episode
            episode_return = self._episode_returns[-1]
            episode_step = self._episode_steps[-1]
            episode_visited_rooms = self._episode_visited_rooms[-1]

            # tracker per step
            self._writer.add_scalar(
                'performance(env_steps)/num_episodes',
                self._total_episodes,
                tb_steps,
            )
            self._writer.add_scalar(
                'performance(env_steps)/episode_return',
                episode_return,
                tb_steps,
            )
            self._writer.add_scalar('performance(env_steps)/episode_steps', episode_step, tb_steps)
            self._writer.add_scalar('performance(env_steps)/episode_visited_rooms', episode_visited_rooms, tb_steps)


class TensorboardStepRateTracker(StepRateTracker):
    """Extend StepRateTracker to write to tensorboard, for single thread training agent only."""

    def __init__(self, writer: SummaryWriter):
        super().__init__()

        self._total_steps = 0  # keep track total number of steps, does not reset
        self._writer = writer

    def step(self, reward, done, info) -> None:
        super().step(reward, done, info)

        self._total_steps += 1

        # To improve performance, only logging at end of an episode.
        if done:
            time_stats = self.get()
            self._writer.add_scalar(
                'performance(env_steps)/step_rate',
                time_stats['step_rate'],
                self._total_steps,
            )


def make_default_trackers(log_dir=None):
    trackers = [
        EpisodeTracker(),
        StepRateTracker(),
    ]

    if log_dir:
        log_dir = Path(f'runs/{log_dir}')

        if not log_dir.exists():
            log_dir.mkdir(parents=True)

        writer = SummaryWriter(log_dir)

        trackers.append(TensorboardEpisodeTracker(writer))
        trackers.append(TensorboardStepRateTracker(writer))

    reset_trackers(trackers)

    return trackers


def reset_trackers(trackers):
    for tracker in trackers:
        tracker.reset()


def set_tracker_steps(trackers, num_steps, num_episodes):
    for tracker in trackers:
        if isinstance(tracker, (TensorboardEpisodeTracker, TensorboardStepRateTracker)):
            tracker._total_steps = num_steps
            tracker._total_episodes = num_episodes


def generate_statistics(trackers):
    """Generates statistics from a sequence of timestep and actions."""
    # Merge all statistics dictionaries into one.
    statistics_dicts = (tracker.get() for tracker in trackers)
    return dict(collections.ChainMap(*statistics_dicts))
