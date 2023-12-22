# Copyright (c) 2023 Michael Hu.
# This code is part of the book "The Art of Reinforcement Learning: Fundamentals, Mathematics, and Implementation with Python.".
# See the accompanying LICENSE file for details.


import plot_lib


if __name__ == '__main__':
    experiments = [
        dict(
            agent_id='reinforce',
            env_name='cartpole',
            base_path='./logs/reinforce/cartpole/',
        ),
        dict(
            agent_id='reinforce_baseline',
            env_name='cartpole',
            base_path='./logs/reinforce_baseline/cartpole/',
        ),
    ]

    plot_lib.plot_and_save_experiments(experiments)
