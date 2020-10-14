# Plans2

**Planning Nature-based Solutions** (**Plans**) is a modelling framework for planning the expansion of nature-based solutions in watersheds.

### Why the "2" on "Plans2"?
**Plans** was born within the scope of a master's degree research project, by 2018. While **Plans1** was just a handful of python scripts, **Plans2** has an application-like structure.

## What is included in this repository

- [x] The python files required to run Plans2;
- [x] A directory called 'samples' with examples of all input files;
- [ ] A 'Handbook' in PDF format.

## Python and packages required

Plans2 is built on top of:
* [Python 3.8](https://www.python.org/downloads/)
* [Numpy](https://numpy.org/)
* [Pandas](https://pandas.pydata.org/)
* [Matplotlib](https://matplotlib.org/)
* [Scipy](https://www.scipy.org/)

## How to install and run Plans2

### Step 1: install Python 3.8
Go to https://www.python.org/downloads/ and download it. Make sure you add Python to PATH (checkbox on the installation wizard).

### Step 2: install the packages
To run Plans2 you need Numpy, Pandas, Matplotlib and Scipy. If you do not have it already installed, you can do that by using terminal or an IDE, like Pycharm.

On Windows terminal:

`C:\Windows\System32\python -m pip install --upgrade pip` (this will update pip)

then:
`C:\Windows\System32\python -m pip install numpy`

then:
`C:\Windows\System32\python -m pip install pandas`

then:
`C:\Windows\System32\python -m pip install matplotlib`

and then:
`C:\Windows\System32\python -m pip install scipy`

### Step 3: download a clone of this repository
Download the ZIP file for the entire repository. Extract the files on any diretory of your machine.

### Step 4: execute the `Run.py` file
Double-click on `Run.py` and it will run the application. 
Alternatively, you may create a python file on the same directory and write the following code:

```python
from tui import main  # this imports the main() function from module tui.py

main()  # call the main() function

```

## Modules of Plans2

### `tui.py`
The frontend of Plans2 is handled by the `tui.py` module. The interface is a simple terminal-based user interface that presents menus for the user.

### `plans2.py`
The general backend tasks of Plans2 is handled by the `plans2.py` module. It performs the silent routines of input, output and process execution. 

### `dp.py`
This module holds the  Dynammic Programming (DP) optimisation algorithm of Plans2  

### `scenarios.py`
text

### `hydrology.py`
text

### `viz.py`
text

### `tools`
text

## Structure of a Plans2 Project

text

## The Terminal-based interface (TUI)

text

## IO files


## Input files documentation

text

## Output files documentation

text

##
