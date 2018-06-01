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
    def __init__(self, what):
        self.what = what
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
        directory = 'src/'

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
    state = BuildState(what)
    state.oh_never_mind()

def has_source_code_tree_changed(what):
    state = BuildState(what)
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

def execute_with_environment(command, env):
    nose_process = os.subprocess.Popen(command.split(" "), env=env)
    nose_process.communicate()  # wait