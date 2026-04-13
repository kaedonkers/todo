# todo: A To-Do List API

This project is a Python package which exposes an API backend for a To-Do List application.

## Installation
`pixi` is a commandline tool used to manage the package dependencies in this Python project. 
It installs packages from both `conda` channels and PyPI.
If it is not already available on your system, please follow the instructions at https://pixi.prefix.dev/latest/installation.

The easiest way to install `pixi` on Linux/MacOS is:
```
curl -fsSL https://pixi.sh/install.sh | sh
```
Once `pixi` is installed, you can clone this repository and install `todo` with the following:
```
git clone https://github.com/kaedonkers/todo.git

cd todo

pixi run install
```

## Quickstart
Once installed, you can launch the `todo` API from your commandline:
```
pixi run start --port 8282
```
This will run the API at `http://localhost:8282/`, where it will listen for requests.

Here is a list of the available options to run `todo`:
```
...
```