# Chapter 2 - Markov Decision Processes

This folder includes the following module:
* `returns.py` implements the code for computing the discounted return


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


Here's an example of how to execute the module for computing discounted returns in chapter 2.
```
cd <repo_path_on_your_computer>/chapter_2

pip3 install -r requirements.txt

python3 -m returns
```


### Execute the code on Jupyter or Google Colab notebooks
Here's an example of how to execute the module on Jupyter or Google Colab notebooks. Please ensure that you have uploaded all the necessary module files to the server before proceeding. And you may need to restart the runtime after installing the required packages.
```
!pip3 install -r requirements.txt

!python3 -m returns
```

#### Important Note:
* It is recommended to run the modules by following the provided example instead of copying and pasting code into Jupyter or Google Colab notebooks. Copying code may lead to errors due to missing parts or incorrect indentation.
* If you encounter errors like 'DuplicateFlagError' while running the modules in Jupyter or Google Colab notebooks, please **restart the kernel or runtime before executing the module**. This issue arises because Jupyter and Google Colab notebooks reuse the Python environment, causing all definitions from the first module run to persist when running the second one.
