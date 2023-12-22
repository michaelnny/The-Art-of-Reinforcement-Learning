# Copyright (c) 2023 Michael Hu.
# This code is part of the book "The Art of Reinforcement Learning: Fundamentals, Mathematics, and Implementation with Python.".
# See the accompanying LICENSE file for details.


import plot_lib


if __name__ == '__main__':
    experiments = [
        dict(
            agent_id='dueling_dqn',
            env_name='riverraid',
            base_path='./logs/dueling_dqn/riverraid/',
        ),
    ]

    plot_lib.plot_and_save_experiments(experiments)
