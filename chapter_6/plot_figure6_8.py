# Copyright (c) 2023 Michael Hu.
# This code is part of the book "The Art of Reinforcement Learning: Fundamentals, Mathematics, and Implementation with Python.".
# See the accompanying LICENSE file for details.


import plot_lib


if __name__ == '__main__':
    experiments = [
        dict(
            agent_id='linear_mc',
            env_name='cartpole',
            base_path='./logs/linear_mc/cartpole/',
        ),
        dict(
            agent_id='linear_q',
            env_name='cartpole',
            base_path='./logs/linear_q/cartpole/',
        ),
    ]

    plot_lib.plot_and_save_experiments(experiments, show_eval_data=False)
