

============================================================
========================== Contents ========================
============================================================

1) Pixie Python
2) Installing from whl file
3) Downloading the pixie Source Code
4) Atom for python development
5) Unit testing with nose
6) Installing from source code
7) Building a whl package file for distribution
8) Uninstalling a python package
9) Uploading to PyPi


==============================
1) PixiePython
==============================

PixiePython is a python package for handling Pixie data files. On its way to achieving this, it 
will implement a bunch of things (a timeseries class + operations + statistical functions) that 
may be useful even if you're not using Pixie data files.

==============================
2) Installing from whl file
==============================

Kill the whitelisting, then open an Anaconda Prompt and change directories to the location of 
the wheel file (e.g. "pixiepython-0.1-py3-none-any.whl") and then install it using pip using 
the command:

pip install pixiepython-0.1-py3-none-any.whl

==============================
3) Downloading the pixie Source Code
==============================

The Pixie .Net code is in a Hg repository hosted at https://bitbucket.org/qld/pixiedatafile
The PixiePython code is held in in a git repository hosted at 

==============================
4) Atom for python development
==============================

I put Atom on my computer by downloading the zipped build "atom-windows.zip" from GitHub and 
unzipping it into a whitelist-excempt location on my D drive. The GitHub page is here:
https://github.com/atom/atom/releases/latest

In Atom you can open a "Project" (basically a folder). When you do this the folder contents 
will be shown in a panel on the left of the GUI. Atom will automatically detect the presence 
of a git repo, and colour-code the files to indicate their state as you work.

==============================
5) Unit testing with nose
==============================

To run the tests it's just a matter of running this from the root of the
repository:
  >pip install nose
  >nosetests
More details here:
https://python-packaging.readthedocs.io/en/latest/testing.html
Here is a video if you like that kinda thing:
https://www.youtube.com/watch?v=qDTg_awHVmw

==============================
6) Installing from source code
==============================

Kill the whitelisting, then open an Anaconda Prompt and change directories to the root of 
the repository (where the setup.py file is) and then run the following command:

  pip install .

If you want to read more, here are the instructions I followed:
  https://python-packaging.readthedocs.io/en/latest/minimal.html

==============================
7) Building a whl package file for distribution
==============================

First of all, you will have to have recent versions of the following python packages:
  https://pypi.org/project/PyHamcrest/
  https://pypi.org/project/setuptools/
  https://pypi.org/project/wheel/
Once you have them installed you can proceed to the next step.

Kill the whitelisting, then open an Anaconda Prompt and change directories to the root of 
the repository (where the setup.py file is) and then run the following command:

  python setup.py bdist_wheel. 

If you want to read more, here are the instructions I followed:
  https://dzone.com/articles/executable-package-pip-install

=================================
8) Uninstalling a python package
=================================
  >pip uninstall pyqhtools

Why uninstall packages? You may have to manually uninstall your package if you want to 
install a newer one which (due to your laziness) has the same build number.

==================================
9) How to upload your package to PyPi
==================================
Create an account on PyPi.
Register your package and upload the relevant metadata by running this:
  >python setup.py register
If you want to upload your package to PyPi so people can install it directly
from there instead of needing to go and clone it from github, then you can use
the following command to register, zip, and upload the package to PyPi in one
step:
  >python setup.py register sdist upload
**** I HAVE CREATED AN ACCOUNT BUT THIS ISN'T WORKING FOR ME



