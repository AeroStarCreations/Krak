# Virtual Environment
__Name:__ kraken

This project is configured to use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

Sometimes the REST documentation is vague. For example, response keys are undefined single letters (e.g. "a"). To learn what keys mean, the [websockets documention](https://docs.kraken.com/websockets/) may have the info.

__To switch to the virtual environment:__

```
$ workon kraken
```

__Virtual environments directory:__

Examples:
* `/Users/<username>/Documents/code/Envs`
* `/Users/<username>/.virtualenvs`

You can view this via the terminal by executing the following:

```
$ echo $WORKON_HOME
```

__To see the current virtual environment:__

```
$ echo $VIRTUAL_ENV
```

To execute python files in VS Code, you will need to set the environment. Do this by typing Command-Shift-P then selecting "Python: Select Interpreter". If the correct environment is not listed, simply enter the value of $VIRTUAL_ENV.

__List of packages in project:__

```
$ lssitepackages
```

__Exit the environment__:

```
$ deactivate
```

# Kraken API

The code will be built on the Kraken REST API ([documentation](https://docs.kraken.com/rest/)).

# Private Environment Variables

API keys should be kept secret and never included in code files or any shared files. For this project, API keys will be put in a `.env` file and accessed using the Python `dotenv` package. The `.env` file should always be listed in the `.gitignore` file. Your `.env` file should be formatted like the following:

```
PUBLIC_KEY=<your public key>
PRIVATE_KEY=<your private key>
```

# Modifying Dependencies

If you add, edit, or remove dependencies, you must update `requirements.txt` as part of the commit.
```
pip freeze --local > requirements.txt
```

# Workspace Setup

1. Install Python and Pip (3.8 or higher)
2. Install and configure virtualenvwrapper ([docs](https://virtualenvwrapper.readthedocs.io/en/latest/))
  1. `pip install virtualenvwrapper`
  2. `mkvirtualenv krak`
  3. `workon krak`
3. Clone git repo (from desired directory)
  1. `git clone https://github.com/AeroStarCreations/Krak.git`
4. Install project dependencies
  1. `pip install -r requirements.txt`