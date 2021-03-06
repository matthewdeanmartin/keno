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

Loading packages is often surprsing.
"""
# import os
# os.environ["PYTHONPATH"] = "."
#
# from pynt_extras import *

import json
from pyntcontrib import *




PROJECT_NAME = "keno"
IS_TRAVIS = 'TRAVIS' in os.environ
if IS_TRAVIS:
    PIPENV = ""
else:
    PIPENV = "pipenv run"
# generic for multi-targeting
PYTHON = "python"
LIBS = ""

from semantic_version import Version

# coding=utf-8
"""
Pynt was missing some things I desperately wanted.
"""
import os

from checksumdir import dirhash

CURRENT_HASH = None

# bash to find what has change recently
# find src/ -type f -print0 | xargs -0 stat -f "%m %N" | sort -rn | head -10 | cut -f2- -d" "
class BuildState(object):
    def __init__(self, what, where):
        self.what = what
        self.where = where
        if not os.path.exists(".build_state"):
            os.makedirs(".build_state")
        self.state_file_name = ".build_state/last_change_{0}.txt".format(what)

    def oh_never_mind(self):
        """
        If a task fails, we don't care if it didn't change since last, re-run,
        :return:
        """
        os.remove(self.state_file_name)

    def has_source_code_tree_changed(self):
        """
        If a task succeeds & is re-run and didn't change, we might not
        want to re-run it if it depends *only* on source code
        :return:
        """
        global CURRENT_HASH
        directory = self.where

        if CURRENT_HASH is None:
            CURRENT_HASH = dirhash(directory, 'md5', excluded_files="*.pyc")

        if os.path.isfile(self.state_file_name):
            with open(self.state_file_name, "r+") as file:
                last_hash = file.read()
                if last_hash != CURRENT_HASH:
                    file.seek(0)
                    file.write(CURRENT_HASH)
                    file.truncate()
                    return True
        else:
            with open(self.state_file_name, "w") as file:
                file.write(CURRENT_HASH)
                return True
        return False

def oh_never_mind(what):
    state = BuildState(what, "keno")
    state.oh_never_mind()

def has_source_code_tree_changed(what):
    state = BuildState(what, "keno")
    return state.has_source_code_tree_changed()

import functools


def skip_if_no_change(name):
    # https://stackoverflow.com/questions/5929107/decorators-with-parameters
    def real_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not has_source_code_tree_changed(name):
                print("Nothing changed, won't re-" + name)
                return
            try:
                return func(*args, **kwargs)
            except:
                oh_never_mind(name)
                raise
        return wrapper
    return real_decorator


import subprocess



def execute_with_environment(command, env):
    nose_process = subprocess.Popen(command.split(" "), env=env)
    nose_process.communicate()  # wait


def execute_get_text(command):
    try:
        completed = subprocess.run(
            command,
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as err:
        raise
    else:
        # print('returncode:', completed.returncode)
        # print('Have {} bytes in stdout: {!r}'.format(
        #     len(completed.stdout),
        #     completed.stdout.decode('utf-8'))
        # )
        return completed.stdout.decode('utf-8')

@task()
#@skip_if_no_change("bumpversion")
def bumpversion():
    """
    Fails if git isn't committed.
    :return:
    """
    # hide until fixed.
    return
    x = execute_get_text(" ".join(["python", "-c", '"import keno;print(keno.__version__)"']))
    print(x)
    current_version = Version(x)
    # new_version = Version("{0}{1}{2}".format(current_version.major, current_version.minor, current_version.build +1))
    # bumpversion --new-version 2.0.2 build --no-tag  --no-commit
    execute("bumpversion", "--current-version", str(current_version), "build", "--tag", "--no-commit")


@task()
@skip_if_no_change("clean")
def clean():
    for folder in ["build", "dist", "keno.egg-info"]:
        execute("rm", "-rf", folder)

    try:
        execute("rm", "lint.txt")
    except:
        pass

@task(clean)
@skip_if_no_change("compile")
def compile():
    execute("python", "-m", "compileall", PROJECT_NAME)

@task()
@skip_if_no_change("formatting")
def formatting():
    execute("black", *("{0}".format(PROJECT_NAME).split(" ")))

@task(compile, formatting)
@skip_if_no_change("lint")
def lint():
    # sort of redundant to above...
    #
    execute("prospector",
            *("{0} --profile keno_style --pylint-config-file=pylintrc.ini --profile-path=.prospector"
              .format(PROJECT_NAME)
              .split(" ")))

    execute("./run_pylint.sh")
    lint_file_name = "lint.txt"
    num_lines = sum(1 for line in open(lint_file_name)
                    if "*************" not in line
                    and "---------------------" not in line
                    and "Your code has been rated at" not in line
                    and "TODO:" not in line)

    fatal_errors = sum(1 for line in open(lint_file_name)
                       if "no-member" in line)

    if fatal_errors > 0:
        for line in open(lint_file_name):
            if "no-member" in line:
                print(line)

        raise TypeError("Fatal lint errors : {0}".format(fatal_errors))

    if num_lines> 100:
        raise TypeError("Too many lines of lint : {0}".format(num_lines))

@task(lint)
@skip_if_no_change("nose_tests")
def nose_tests():
    # if these were integration tests with say, API calls, we might not want to skip
    execute("python", "-m", "nose", PROJECT_NAME)

@task(nose_tests)
@skip_if_no_change("coverage")
def coverage():
    # if these were integration tests with say, API calls, we might not want to skip
    execute("py.test", *("keno --cov=keno --cov-report html:coverage --verbose".split(" ")))

@task(nose_tests)
@skip_if_no_change("docs")
def docs():
    with safe_cd("docs"):
        execute("make", "html")

@task()
@skip_if_no_change("pip_check")
def pip_check():
    execute("pip", "check")
    execute("safety", "check")
    execute("safety", "check", "-r", "requirements-dev.txt")

@task(pip_check)
def pin_dependencies():
    execute(*("{0} pipenv_to_requirements".format(PIPENV).strip().split(" ")))

@task()
@skip_if_no_change("compile_md")
def compile_md():
    # if IS_TRAVIS:
    #     # pandoc doesn't appear to work on travis for python
    #     return
    execute("pandoc", *("--from=markdown --to=rst --output=README.rst README.md".split(" ")))

@task()
@skip_if_no_change("mypy")
def mypy():
    if IS_TRAVIS:
        command = "{0} -m mypy {1} --ignore-missing-imports --strict".format(PYTHON, PROJECT_NAME).strip()
    else:
        command = "{0} mypy {1} --ignore-missing-imports --strict".format(PIPENV, PROJECT_NAME).strip()

    env = config_pythonpath()
    bash_process = subprocess.Popen(command.split(" "),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    env=env
                                    )
    out, err = bash_process.communicate()  # wait
    errors_file_name ="mypy_errors.txt"
    with open(errors_file_name, "w+") as errors_file:
        lines = out.decode().split("\n")
        for line in lines:
            if "test.py" in line:
                continue
            if "tests.py" in line:
                continue
            if "/test_" in line:
                continue
            if "/tests_" in line:
                continue
            else:
                errors_file.writelines([line + "\n"])

    num_lines = sum(1 for line in open(errors_file_name) if line)
    if num_lines > 20:
        raise TypeError("Too many lines of mypy : {0}".format(num_lines))


@task()
def detect_secrets():
    # use
    # blah blah = "foo"     # pragma: whitelist secret
    # to ignore a false posites
    command = "detect-secrets --scan --base64-limit 3.5"
    bash_process = subprocess.Popen(command.split(" "),
                                    # shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE
                                    )
    out, err = bash_process.communicate()  # wait
    errors_file = "detect-secrets-results.txt"
    with open(errors_file, "w+") as file_handle:
        file_handle.write(out.decode())

    with open(errors_file) as f:
        data = json.load(f)
    if data["results"]:
        for result in data["results"]:
            print(result)
        raise TypeError("detect-secrets has discovered high entropy strings, possibly passwords?")


def config_pythonpath():
    my_env = {**os.environ}
    my_env["PYTHONPATH"] = my_env.get("PYTHONPATH",
                                      "") + LIBS
    print(my_env["PYTHONPATH"])
    return my_env

@task(mypy, detect_secrets, pin_dependencies, docs, nose_tests, pip_check, compile, lint, compile_md)
@skip_if_no_change("package")
def package():
    execute("python", "setup.py", "sdist", "--formats=gztar,zip")

@task()
def xar():
    # If you have homebrew installed, it's as easy as running brew
    compression_format = "gzip" # zstd
    command = "{0} setup.py bdist_xar --xar-compression-algorithm={1}".format(PYTHON, compression_format)
    execute(*(command.split(" ")))
    print("xar requires some complex installation https://code.fb.com/data-infrastructure/xars-a-more-efficient-open-source-system-for-self-contained-executables/")

@task()
def py2app():
    command = "{0} setup.py py2app".format(PYTHON).strip()
    execute(*(command.split(" ")))

@task()
def echo(*args, **kwargs):
    print(args)
    print(kwargs)


# Default task (if specified) is run when no task is specified in the command line
# make sure you define the variable __DEFAULT__ after the task is defined
# A good convention is to define it at the end of the module
# __DEFAULT__ is an optional member

__DEFAULT__ = echo

