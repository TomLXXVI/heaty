## HEATY

### Author
Tom Christiaens. Have a look at [http://www.dirkchristiaens.be](http://www.dirkchristiaens.be).


### About
Heaty is a building heat load calculator that implements the "standard method" set 
out in the European standard EN 12831-1:2017, section 6.


### Installation and Usage
Heaty's source code is available at [https://github.com/TomLXXVI/heaty](https://github.com/TomLXXVI/heaty).

Several installation options are available:

**Option 1**<br>
If you have Python installed on your computer, you can clone the repository or download it as a ZIP-file 
from GitHub. After that, you need to create a source or built distribution using the *setup.py* file in the repository. 
To do this, after cloning or unzipping the remote repository on your local computer, step into your 
local repository folder and type at the command prompt:
```
python setup.py sdist
```
to create a source distribution (`Heaty-2020.10b1.tar.gz`), or, if if you have *wheel* installed, you can also type:
```
python setup.py bdist_wheel
```
to create a wheel distribution (`Heaty-2020.10b1-py3-none-any.whl`).<br>
You can then use this distribution file in your own project by taking the following steps:
- Create a new project folder.
- Create a virtual environment and activate it.
- Copy the distribution file into your project folder.
- Type e.g. `pip install Heaty-2020.10b1.tar.gz` to install the distribution in the virtual environment of your project.
- Type `heaty` at the command prompt in your project folder to launch the GUI-program.

**Option 2**<br>
You can find Heaty also on PyPi. To install the distribution package directly from Pypi, create your 
project folder and virtual environment as described under option 1, and type `pip install heaty` at the command prompt.
When *pip* is finished, type `heaty` at the command prompt in your project folder to launch the GUI-program.

**Option 3**<br> 
Windows 10 users can download from GitHub, under the folder *executable* a ZIP-file *heaty.zip* that
contains the EXE-file *heaty.exe*. Save the ZIP-file anywhere you want on your computer and unzip it there. The result 
will be a self-contained application folder *heaty*. In this folder, double click *heaty.exe* to launch the GUI
program.

Once Heaty is running, further explanation about what Heaty can do and how to use it can be found under the *Help* menu 
of the running program, under *User Guide*. The user guide is a PDF-document that will be opened in your standard 
PDF-reader or web browser.


### Notes
"Heaty" has been developed with Python 3.8 on a Windows 10 computer.
