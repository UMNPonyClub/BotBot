#!/usr/bin/python

import os, stat, sys
import checker

from enum import Enum

import problems

# Holds a set of checks that can be run on a file to make sure that
# it's suitable for the shared directory. Runs checks recursively on a
# given path.
class Checker:
    # A set of all the checking functions this checker knows of.  All
    # checkers return a number signifying a specific problem with the
    # file specified in the path.
    def __init__(self):
        self.checks = set()
        self.all_problems = list()

    # Add a new checking function to the set, or a list/tuple of functions.
    def register(self, fn):
        if isinstance(fn, list) or isinstance(fn, tuple):
            for f in fn:
                self.checks.add(f)
        else:
            self.checks.add(fn)

    # Helper function to get the file mode bits
    def get_mode_bits(self, path):
        return os.stat(path).st_mode

    # Run all the checks on every file in the specified path,
    # recursively. Returns a list of tuples. Each tuple contains 2
    # elements: the first is the path of the file, and the second is a
    # list of issues with the file at that path.
    def check_tree(self, path):
        self.all_problems = list()

        for f in os.listdir(path):
            newpath = os.path.join(path, f)
            np_mode = self.get_mode_bits(newpath)

            if stat.S_ISDIR(np_mode):
                self.check_tree(newpath)
            else:
                current_problems = list()
                for check in self.checks:
                    current_problems.append(check(np_mode))

                self.all_problems.append((newpath, current_problems))

    def pretty_print_issues(self):
        for p in self.all_problems:
            for m in p[1]:
                print(p[0] + ": " + m.message + " " + m.fix)

def main():
    checker_list = [checker.permission_issues]
    c = Checker()
    c.register(checker_list)
    c.check_tree('.')
    c.pretty_print_issues()

if __name__ == '__main__':
    main()