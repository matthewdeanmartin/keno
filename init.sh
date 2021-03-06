#!/usr/bin/env bash
set -e

create_it_pipenv_style()
{
    pipenv install
    pipenv shell
}

create_it_conda_style()
{
    export PATH="$HOME/miniconda3/bin:$PATH"
    conda create --name keno_conda_env
    . activate keno_conda_env
    conda env list
}
activate_it()
{
    export PATH="$HOME/miniconda3/bin:$PATH"
    # conda create --name keno_conda_env
    . activate keno_conda_env
    conda env list
}

dev_installs()
{
    # pyflakes for some reason hangs if not using no-cache-dir
    pip install -r requirements_dev.txt --no-cache-dir
}

conda_installs()
{
    conda install numpy cython
}