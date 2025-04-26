# Sudoku Solver

Solves Sudoku from sizes 9x9 to 81x81

## Description

Sudoku Solver has the capabilities to generate a proper and solvable sudoku table, ranging in sizes 9x9 to 81x81, and utilizes two solvers, one being a Z3 solver and one a PYSAT solver. Both solvers utilize CNF to convert the UI capabilities to applicable data structures for solver utilization and back to UI applicability. The UI, a tksheets extension, allows for the board to be displayed, interactive tools to choose a type of solver (Z3 or PYSAT) and displays to the user the solved board and the time used by the AI to solve the sudoku. The user can also choose the size of the sudoku board via a sliding option at the top of the tab. 

## Getting Started

### Dependencies

* Windows 10, MacOS, or Ubuntu-22.04 
* Visual Studio Code (or other compiler)
* Git/GitHub capabilities
* Python Installation:
  
  Debian/Ubuntu/MacOS:
    - Update your package list:
      ```
      sudo apt update
      ```
    - Install pip for Python 3:
      ```
      sudo apt install python3-pip
      ```
      
  CentOS/RHEL/Fedora:
    - Enable the EPEL repository:
      
      ```
      yum install epel-release (or dnf install epel-release for Fedora)
      ```
    - Install pip for Python 3:
      ```
       yum install python3-pip (or dnf install python3-pip for Fedora)
      ```
      
Arch Linux:
  ```
  pacman -S python-pip
  ```

openSUSE:
```
  zypper install python3-pip
```
* Libraries needed from PIP:
  
  Z3-Solver:
  ``` 
    pip install z3-solver
  ```
  
  PYSAT:
  ```
    pip install python-sat
  ```
  
  tksheet:
  ```
    pip install tksheet
  ```

  IF YOUR PYTHON INSTALLATION 
DOESN'T ALREADY HAVE tkinter:
  ```
    pip install tkinter
  ```


### Installing

* Run basic Git clone command
  ```
  git clone <repo-name>
  ```

### Executing program

* VSCode or other compiler options:
  - On compiler, open graphics.py
  - if installations above worked correctly, there should be no errors in the libraries indicated at top of file.
  -  Run python (indicated by play button at top of VSCode) and screen will appear.
* Command line:
  - Ensure the terminal line is inside the correct repository (SudokuSolver_cpts440)
  - Example:
    ```
    ~/SudokuSolver_cpts440
    ```
  - run following command:
    ```
    python graphics.py
    ```
  - screen will appear
* select size of sudoku, type of solver, and hit solve.
* Warning: Larger Sudoku take much longer to complete.


## Authors
Emily Porter,
Claire Monson,
Shampurna Das,
Preston Livingston,
Brian Mcclosky,
Brenden Darnell



