# Chapter 13 - Curiosity-Driven Exploration

This folder includes the following module:
* `ppo_rnd.py` implements the code for the distributed PPO algorithm with RND module
* `ppo_rnd_atari.py` a driver program which uses the distributed PPO algorithm with RND module to solve Atari video game Montezuma's Revenge
* `eval_agent.py` a driver program which loads the trained PPO neural network to play and record a video of the Atari video game Montezuma's Revenge
* `gym_env_processor.py` contains functions for environment pre-processing, such as frame resizing, frame stacking, and frame skipping, specifically designed for Atari video games
* `trackers.py` contains code for tracking statistics during training and evaluation
* `normalizer.py` contains code for normalize data like environment observation for RND module



## How to run the code
Please note that the code requires Python 3.10.6 or a higher version to run.

### Important Note:
* The code in this directory was not designed to be executed on Jupyter or Google Colab notebooks due to its high computational demands.
* The 'eval_agent.py' module may not work on Jupyter or Google Colab notebooks. This is because these environments are 'headless,' lacking a display, which could potentially prevent video recording of the game.
* It is crucial to acknowledge that training a PPO agent with curiosity-driven exploration module on the Montezuma's Revenge Atari game can often be a time-consuming process, often requiring hours or even days. The duration of training depends on various factors, such as the the computer hardware being used, number of actors running in parallel.


Before you get started, ensure that you have the latest version of pip installed on your machine by executing the following command:
```
python3 -m pip install --upgrade pip setuptools
```

To run the code, follow these steps:

1. Open the terminal application in your operating system.
2. Navigate to the specific chapter where you want to execute the code.
3. Install the required packages by using pip and referencing the `requirements.txt` file.
4. Once the packages are installed, you can proceed to execute the individual modules.


Here's an example of how to execute the module for using distributed PPO algorithm with RND module to solve the Atari video game Montezuma's Revenge in chapter 13.
```
cd <repo_path_on_your_computer>/chapter_13

pip3 install -r requirements.txt

python3 -m ppo_rnd_atari
```

**Using PyTorch with GPUs:**
If you are utilizing Nvidia GPUs, it is highly recommended to install PyTorch with CUDA by following the instructions provided at https://pytorch.org/get-started/locally/.


## Reference Code
* [Deep RL Zoo](https://github.com/michaelnny/deep_rl_zoo)
* [Baselines](https://github.com/openai/baselines)
