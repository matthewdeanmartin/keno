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
    pip install -r requirements_dev.txt
}

conda_installs()
{
    conda install numpy cython
}

go