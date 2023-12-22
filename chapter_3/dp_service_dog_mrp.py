# Copyright (c) 2023 Michael Hu.
# This code is part of the book "The Art of Reinforcement Learning: Fundamentals, Mathematics, and Implementation with Python.".
# See the accompanying LICENSE file for details.


"""
Sample code of using DP algorithms to solve the service dog MRP example.
"""
from envs.dog_mrp import DogMRPEnv

import utils
import algos

if __name__ == '__main__':
    env = DogMRPEnv()

    for discount in [0, 0.3, 0.5, 0.7, 0.9, 1]:
        state_values = algos.compute_mrp_state_value(env, discount)
        print(f'State value function for service dog example MRP (discount={discount}):')
        utils.print_state_value(env, state_values)
        print('\n')
