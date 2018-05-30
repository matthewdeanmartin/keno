#!/usr/bin/env bash
set -e

go()
{
    export PATH="$HOME/miniconda3/bin:$PATH"
    conda create --name keno_conda_env
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

go