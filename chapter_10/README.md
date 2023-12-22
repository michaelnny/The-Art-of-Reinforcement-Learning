# Chapter 10 - Problems with Continuous Action Space

This folder includes the following module:
* `actor_critic_continuous.py` implements the Actor-Critic algorithm to solve classic robotic control tasks
* `gym_env_processor.py` contains the functions for environment pre-processing like observation normalization and reward normalization for the robotic control tasks
* `trackers.py` contains code for tracking statistics during training and evaluation



## How to run the code
Please note that the code requires Python 3.10.6 or a higher version to run.


### Execute the code on local machine
Before you get started, ensure that you have the latest version of pip installed on your machine by executing the following command:
```
python3 -m pip install --upgrade pip setuptools
```

To run the code, follow these steps:

1. Open the terminal application in your operating system.
2. Navigate to the specific chapter where you want to execute the code.
3. Install the required packages by using pip and referencing the `requirements.txt` file.
4. Once the packages are installed, you can proceed to execute the individual modules.


Here's an example of how to execute the module for using Actor-Critic algorithm to solve the Ant robotic control tasks in chapter 10.
```
cd <repo_path_on_your_computer>/chapter_10

pip3 install -r requirements.txt

python3 -m actor_critic_continuous --environment_name=Ant-v4
```

**Using PyTorch with GPUs:**
If you are utilizing Nvidia GPUs, it is highly recommended to install PyTorch with CUDA by following the instructions provided at https://pytorch.org/get-started/locally/.


### Execute the code on Jupyter or Google Colab notebooks
Here's an example of how to execute the module on Jupyter or Google Colab notebooks. Please ensure that you have uploaded all the necessary module files to the server before proceeding. And you may need to restart the runtime after installing the required packages.
```
!pip3 install -r requirements.txt

!python3 -m actor_critic_continuous --environment_name=Ant-v4
```

#### Important Note:
* It is recommended to run the modules by following the provided example instead of copying and pasting code into Jupyter or Google Colab notebooks. Copying code may lead to errors due to missing parts or incorrect indentation.
* If you encounter errors like 'DuplicateFlagError' while running the modules in Jupyter or Google Colab notebooks, please **restart the kernel or runtime before executing the module**. This issue arises because Jupyter and Google Colab notebooks reuse the Python environment, causing all definitions from the first module run to persist when running the second one.


## Reference Code
* [Deep RL Zoo](https://github.com/michaelnny/deep_rl_zoo)
* [Baselines](https://github.com/openai/baselines)
