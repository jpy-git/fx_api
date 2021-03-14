# Smart Pension - FX API Demo

This project contains:

A. Custom fx_api package - fx_api/

B. Jupyter notebook containing Smart Pension Python test solutions - scripts/

C. Automated unit tests using pytest - tests/

## Setup

Clone project from GitHub repo (https://github.com/jpy-git/fx_api)

Create Python virtual environment in root folder of project. I have developed the package using Python 3.8 so would recommend using the same.

SHELL:
```
<path to Python 3.8 executable> -m venv venv
venv/bin/activate
```

Upgrade pip

SHELL:
```
python -m pip install --upgrade pip
```

Install dependencies. Again I have set specific package versions to ensure a consistent environment. 

SHELL:
```
pip install -r requirements.txt
```

Install custom fx_api package. For simplicity recommend using

SHELL:
```
python setup.py develop
```

Restart shell before proceeding.

## Unit tests

SHELL:
```
pytest
```

## Python exercise

Everything else required for the Python exercise can be found in 

SHELL:
```
python -m notebook "scripts/Smart Pension - FX API demo notebook.ipynb"
```




