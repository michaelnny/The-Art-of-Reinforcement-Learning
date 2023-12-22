# Chapter 6 - Linear Value Function Approximation

This folder includes the following module:
* `envs` contains the classes for MDP environments
* `linear_mc_cartpole.py` implements the Monte Carlo method and Linear-VFA (Value Function Approximation) to solve the cart pole problem
* `linear_q_cartpole.py` implements Q-learning and Linear-VFA to solve the cart pole problem
* `linear_mc_service_dog_mdp.py` implements the Monte Carlo method and Linear-VFA to solve the service dog MDP problem
* `trackers.py` contains code for tracking statistics during training and evaluation
* `tiles3.py` contains code for tile coding, the code was originally developed by Rich Sutton

### Service Dog MDP
<img src="./images/dog_mdp.png" width="600" >


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


Here's an example of how to execute the module for using Q-learning with linear-VFA to solve the Cart Pole problem in chapter 6.
```
cd <repo_path_on_your_computer>/chapter_6

pip3 install -r requirements.txt

python3 -m linear_q_cartpole
```


### Execute the code on Jupyter or Google Colab notebooks
Here's an example of how to execute the module on Jupyter or Google Colab notebooks. Please ensure that you have uploaded all the necessary module files to the server before proceeding. And you may need to restart the kernel (of runtime for Colab) after installing the required packages.
```
!pip3 install -r requirements.txt

!python3 -m linear_q_cartpole
```

#### Important Note:
* It is recommended to run the modules by following the provided example instead of copying and pasting code into Jupyter or Google Colab notebooks. Copying code may lead to errors due to missing parts or incorrect indentation.
* If you encounter errors like 'DuplicateFlagError' while running the modules in Jupyter or Google Colab notebooks, please **restart the kernel or runtime before executing the module**. This issue arises because Jupyter and Google Colab notebooks reuse the Python environment, causing all definitions from the first module run to persist when running the second one.


## Reference Code
* [Tile Coding](http://incompleteideas.net/book/the-book-2nd.html)
