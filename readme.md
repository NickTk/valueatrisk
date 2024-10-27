1. The Repo contains jupyter notebooks that implement the 'option' and the 'valuetrisk' tasks respectively. 

2. If there is a problem running notebook cells (for example 'module not found' error),
you need to create virtual environment from the configuration file, select the created environment and run the notebook from it. 
To create the environment, type in the command line from within the project root folder:

conda env create -f environment.yml

After that, choose the conda environment in your editor by the name 'varcalc'

3. To run the vanilla option test, type in the command line from within the project root folder:

pytest models.test.py

If the 'pytest' command is not found, create the environment as in the item 2.
