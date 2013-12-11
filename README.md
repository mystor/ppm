# Python Project Manager
ppm (Python Project Manager) is a simple wrapper around pip and virtualenv which aims to make it easier to manage your python projects.  It removes the need to explicitly enter and exit virtualenvs, and handles basic python version control.

## Install
ppm isn't on pypi yet, so the easiest way to install is to clone this repository, and run `./setup.py install`.  The only file installed is `ppm`, so simply `rm -i $(which ppm)` to remove it.

ppm expects you to have virtualenv and pip installed.  If you don't, then it will probably explode in your face

## Which Environment?
`ppm` will, by default, search the current directory for the `ppm_env` directory.  If that diretcory exists, it will be used as the environment directory for the function.  

If `ppm_env` does not exist, `ppm` will do one of two things:
1. If the function is non-destructive (doesn't change the venv), it will crawl up the directory tree until it finds a `ppm_env` folder or gives up, or
2. If the function is distructive, give up immediately.

If the `-e` command line parameter, the environment specified by `-e` will be used instead of `ppm_env`, and no directory crawling will occur.

## Usage
```bash
ppm init [-e ENV] [-r REQUIREMENT] [-b PYBIN | -V PYVER]
```

`-e ENV`: OPTIONA:, Initialize the given environment (default: `./ppm_env`)
`-r REQUIREMENT`: OPTIONAL, Initialize with the given file (default `./requirements.txt`)
`-V PYVER`: OPTIONAL, Initialize with the given python version
`-b PYBIN`: Initialize with the given python binary

You shouldn't have to run this command unless you want to specify an alternate requirements file, python binary, or python version to set up your environment with.  Other functions will automatically initialize the environment automatically.

```bash
ppm install [-e ENV] ...
```

`-e ENV`: OPTIONAL, Environment to install into (default: `./ppm_env`)

Initializes (if necessary) and loads the environment specified by `-e`.  Then executes `pip install` in the environment, passing the remainder of the arguments.

```bash
ppm uninstall [-e ENV] ...
```
Like `ppm install`, but executes `pip uninstall` in the environment.

```bash
ppm run [-e ENV] ...
```
Initializes (if necessary) and loads the environment specified by `-e`.  Then executes `python` passing the remainder of the arguments

```bash
ppm shell [-e ENV]
```
Launches an interactive python shell in the current directory within the specified virtualenv


