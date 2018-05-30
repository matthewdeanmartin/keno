# coding=utf-8
"""
Trying out pynt.

mini-first-impressions review:
- good build dependencies
- easy to call python things
- cumbersome to call things normally done in bash.
- if I actually used it, I would probably have 50% of code in tiny bash scripts, 1 per task.
- loops, if-blocks, etc less painful than bash.
- no easy way to redirect output of script to file
- no way to use this to set up venvs, nor to do deployment (needs venv to run this!)
"""
from pynt import task
from pyntcontrib import execute, safe_cd
from pathlib import Path

PROJECT_NAME = "keno"

@task()
def clean():
    for folder in ["build", "dist", "keno.egg-info"]:
        execute("rm", "-rf", folder)

    execute("rm", "lint.txt")

@task(clean)
def compile():
    execute("python", "-m", "compileall", PROJECT_NAME)

@task(compile)
def lint():
    # if not Path(".rcfile=pylintrc.ini").is_file():
    #     execute("pylint", "--generate-rcfile>pylintrc.ini")
    #
    # execute("lint_it.sh","--rcfile=pylintrc.ini>lint.txt" )
    execute("./run_pylint.sh")

    num_lines = sum(1 for line in open('lint.txt'))
    if num_lines> 100:
        raise TypeError("Too many lines of lint : {0}".format(num_lines))


@task(lint)
def nose_tests():
    execute("python", "-m", "nose", PROJECT_NAME)

@task(nose_tests)
def coverage():
    execute("py.test", *("keno --cov=keno --cov-report html:coverage --verbose".split(" ")))

@task(nose_tests)
def docs():
    with safe_cd("docs"):
        execute("make", "html")

@task()
def pip_check():
    execute("pip", "check")

@task(docs, nose_tests, pip_check, compile, lint)
def package():
    execute("pandoc", *("--from=markdown --to=rst --output=README.rst README.md".split(" ")))
    execute("python", "setup.py", "sdist")

@task()
def echo(*args, **kwargs):
    print(args)
    print(kwargs)


# Default task (if specified) is run when no task is specified in the command line
# make sure you define the variable __DEFAULT__ after the task is defined
# A good convention is to define it at the end of the module
# __DEFAULT__ is an optional member

__DEFAULT__ = echo
