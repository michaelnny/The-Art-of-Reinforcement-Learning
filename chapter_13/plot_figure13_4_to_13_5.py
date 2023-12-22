# Copyright (c) 2023 Michael Hu.
# This code is part of the book "The Art of Reinforcement Learning: Fundamentals, Mathematics, and Implementation with Python.".
# See the accompanying LICENSE file for details.


import plot_lib


if __name__ == '__main__':
    experiments = [
        dict(
            agent_id='ppo_rnd_32actors',
            env_name='montezumarevenge',
            base_path='./logs/ppo_rnd/montezumarevenge',
        ),
    ]

    plot_lib.plot_and_save_experiments(
        experiments, additional_columns=['train_episode_visited_rooms', 'eval_episode_visited_rooms']
    )
