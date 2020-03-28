# gis-tools


### ArcGIS Pro Environments

Settings > Python > Manage Environments > Clone Default

*This creates a virtual environment in user directory that will be detected by Anaconda Navigator. Packages can be added without damage to the default ArcGIS Pro python installation.*


### Anaconda Setup

[Anaconda](https://www.anaconda.com)

[Installing on Windows](https://docs.anaconda.com/anaconda/install/windows/)

*We recommend not adding Anaconda to the PATH environment variable, since this can interfere with other software. Instead, use Anaconda software by opening Anaconda Navigator or the Anaconda Prompt from the Start Menu.*

In Anaconda Navigator the ArcGIS Pro cloned environment can be selected to seed vscode with the correct python path to the ArcGIS Pro virtual environment. When setup correctly start vscode with Anaconda Navigator.


### vscode setup

Assumes that ArcGIS python environments will be used.

To select a specific environment, use the Python: Select Interpreter command from the Command Palette (`Ctrl+Shift+P`). Select the ArcGIS Pro virtual environment.

Terminal > New Terminal will automatically run conda activate "ArcGIS Pro virtual environment"


**Install Necessary Conda Packages**

```
> conda install -c conda-forge fire
> conda install -c conda-forge yapf
> conda install -c conda-forge beautifulsoup4
```

[python-fire](https://github.com/google/python-fire)

[yapf](https://github.com/google/yapf)

[Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md)

[https://www.crummy.com/software/BeautifulSoup/](https://www.crummy.com/software/BeautifulSoup/)


**Add to .vscode settings.json**

```json
{
    "python.pythonPath": "ArcGIS Pro virtual environment is automatically added",
    "editor.formatOnSave": true,
    "python.formatting.provider": "yapf",
    "python.formatting.yapfArgs": [
        "--style",
        "{based_on_style: pep8}"
    ]
}
```


**To reset vscode back to default**

```
Windows - Delete %APPDATA%\Code and %USERPROFILE%\.vscode. (WinKey + r then run %APPDATA% or %USERPROFILE%)
macOS - Delete $HOME/Library/Application Support/Code and ~/.vscode.
Linux - Delete $HOME/.config/Code and ~/.vscode.
```


### useful commands

**check path variable**

`$Env:path -split ";"`


**check which python**

```python
>>> import os
>>> import sys
>>> os.path.dirname(sys.executable)
```


**comments template**

```python
"""Module summary.

Description sentence(s).
"""

def example():
    """Function summary.

    Description sentence(s).

    Arguments:
        arg 1: Description sentence.
        arg 2: Description sentence.

    Returns:
        Description sentence.

    Raises:
        Description sentence.
    """
    pass
```


### Resources

* [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

* [Writing on GitHub](https://help.github.com/categories/writing-on-github/)

* [vscode python environments](https://code.visualstudio.com/docs/python/environments)

* [About Windows Environment Variables](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7)

* [Python in ArcGIS Pro](https://pro.arcgis.com/en/pro-app/arcpy/get-started/installing-python-for-arcgis-pro.htm)

* [Notebooks in ArcGIS Pro](https://pro.arcgis.com/en/pro-app/arcpy/get-started/pro-notebooks.htm)

* [Introducing ArcGIS Notebooks in ArcGIS Pro](https://www.esri.com/arcgis-blog/products/arcgis-pro/analytics/introducing-arcgis-notebooks-in-arcgis-pro/)

* [ArcGIS API for Python Samples](https://developers.arcgis.com/python/sample-notebooks/)

* [ArcGIS API for Python Samples - on GitHub](https://github.com/Esri/arcgis-python-api)