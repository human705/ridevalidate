# ridevalidate

Validate bike ride data for use in GC

[Anaconda is Bloated - Set up a lean, robust data science environment](https://www.dunderdata.com/blog/anaconda-is-bloated-set-up-a-lean-robust-data-science-environment-with-miniconda-and-conda-forge)

These instructions are based off of the above tutorial

# Download Miniconda:

Anaconda is bloated, just use the command-line to manage all of your environments

[Miniconda - Conda documentation](https://docs.conda.io/en/latest/miniconda.html)

# Use anaconda prompt as admin for all conda commands

```
conda config --set channel_priority strict
```

```
conda install <package-name>
```

# Don't set Anaconda to PATH you should just use the Anaconda Prompt Application:

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6329edef-4a62-4b49-ae73-21a69a76367c/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6329edef-4a62-4b49-ae73-21a69a76367c/Untitled.png)

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f12446f6-9a9d-4de1-b920-33718b738df4/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f12446f6-9a9d-4de1-b920-33718b738df4/Untitled.png)

# Update Anaconda:

```bash
conda update conda
```

# Add conda-forge As a Channel:

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install <package-name>


Setting Up Conda Environment and change minimal-ds to anything you want

# Create a `minimal_ds` Environment:

```bash
conda create --name minimal_ds
```
# Activate `minimal_ds` Environment:

```bash
conda activate minimal_ds
```
````List environments
conda env list

conda deactivate
```
conda env remove -n testpyqt1

````

# Add basic DS Packages:

bash
conda install pandas matplotlib

# conda install pandas scikit-learn matplotlib notebook statsmodels openpyxl xlrd seaborn

pip install fitdecode spicy

```

pip3 freeze > requirements.txt
pip install -r requirements.txt

conda deactivate
```

conda env remove -n testpyqt1


# miniconda to install Python. DO NOT install another python ver (Need to test this)

# New folder structure

# setup for all users

C:\ProgramData\Miniconda3\envs

# If you are working with VS Code you may need to add the path to the environment manually

add the path "C:\Users\%USERNAME%\miniconda3\envs\envname\python.exe"

# Fix missing packeges

# Replace python path with the correct env

> C:/Users/peter/miniconda3/envs/RideFileValidator/python.exe -m pip show lxml
> C:/Users/peter/miniconda3/envs/RideFileValidator/python.exe -m pip install lxml
> C:/Users/peter/miniconda3/envs/RideFileValidator/python.exe -m pip uninstall lxml
