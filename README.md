# ridevalidate

Validate bike ride data for use in GC

[Anaconda is Bloated - Set up a lean, robust data science environment](https://www.dunderdata.com/blog/anaconda-is-bloated-set-up-a-lean-robust-data-science-environment-with-miniconda-and-conda-forge)

These instructions are based off of the above tutorial

# Download Miniconda:

Anaconda is bloated, just use the command-line to manage all of your environments

[Miniconda - Conda documentation](https://docs.conda.io/en/latest/miniconda.html)

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


# Add conda-forge As a Channel:

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install <package-name>
````

# Add basic DS Packages:

bash
conda install pandas scikit-learn matplotlib notebook statsmodels openpyxl xlrd seaborn
pip install fitdecode

```

pip3 freeze > requirements.txt
pip install -r requirements.txt

conda deactivate
```

# If you are working with VS Code you may need to add the path to the environment manually

add the path "C:\Users\%USERNAME%\miniconda3\envs\envname\python.exe"
