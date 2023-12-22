# Chapter 12 - Distributed Reinforcement Learning

This folder includes the following module:
* `ppo.py` implements the code for the distributed PPO algorithm
* `dist_ppo_continuous.py` a driver program which uses the distributed PPO algorithm to solve classic robotic control tasks
* `gym_env_processor.py` contains the functions for environment pre-processing like observation normalization and reward normalization for the robotic control tasks
* `trackers.py` contains code for tracking statistics during training and evaluation



## How to run the code
Please note that the code requires Python 3.10.6 or a higher version to run.

### Important Note:
* The code in this directory was not designed to be executed on Jupyter or Google Colab notebooks due to its high computational demands.
* It is crucial to acknowledge that training a distributed PPO agent can often be a time-consuming process, often requiring hours or even days. The duration of training depends on various factors, such as the the computer hardware being used, number of actors running in parallel.


Before you get started, ensure that you have the latest version of pip installed on your machine by executing the following command:
```
python3 -m pip install --upgrade pip setuptools
```

To run the code, follow these steps:

1. Open the terminal application in your operating system.
2. Navigate to the specific chapter where you want to execute the code.
3. Install the required packages by using pip and referencing the `requirements.txt` file.
4. Once the packages are installed, you can proceed to execute the individual modules.


Here's an example of how to execute the module for using distributed PPO algorithm to solve the Ant robotic control tasks in chapter 12.
```
cd <repo_path_on_your_computer>/chapter_12

pip3 install -r requirements.txt

python3 -m dist_ppo_continuous --environment_name=Ant-v4
```

**Using PyTorch with GPUs:**
If you are utilizing Nvidia GPUs, it is highly recommended to install PyTorch with CUDA by following the instructions provided at https://pytorch.org/get-started/locally/.


## Reference Code
* [Deep RL Zoo](https://github.com/michaelnny/deep_rl_zoo)
* [Baselines](https://github.com/openai/baselines)
