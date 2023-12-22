# Copyright (c) 2023 Michael Hu.
# This code is part of the book "The Art of Reinforcement Learning: Fundamentals, Mathematics, and Implementation with Python.".
# See the accompanying LICENSE file for details.


import os

os.environ['BOARD_SIZE'] = str(9)
from eval_dataset import build_eval_dataset
from util import create_logger

if __name__ == '__main__':
    logger = create_logger('DEBUG')
    eval_dataset = build_eval_dataset('./pro_games/go/9x9', num_stack=8, logger=logger)
    # eval_dataset = build_eval_dataset('./9x9_matches', num_stack=8, logger=logger)
