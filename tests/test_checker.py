import pytest
import os, stat

from botbot import checker, problems, checks

# Tests for Checker class methods
def test_checker_register_accept_single_function():
    c = checker.Checker()
    c.register(lambda: print("Hello world!"))
    assert len(c.checks) == 1

def test_checker_register_accept_function_list():
    c = checker.Checker()

    # Function list
    f = list()
    f.append(lambda : print("Hello world!"))
    f.append(lambda i : i + i)
    c.register(f)

# Tests for checking functions

def test_symlink_checker_same_directory(tmpdir):
    prev = tmpdir.chdir()
    f = tmpdir.join('file.txt')
    f.write('')
    os.symlink(f.basename, 'link')

    assert not checker.is_link(f.basename)
    assert checker.is_link('link')
    prev.chdir()

def test_symlink_checker_link_in_lower_directory(tmpdir):
    prev = tmpdir.chdir()
    f = tmpdir.join('file.txt')
    f.write('')

    os.mkdir('newdir')
    os.symlink(f.basename, os.path.join('newdir', 'link'))

    assert checker.is_link(os.path.join('newdir', 'link'))
    assert not checker.is_link(f.basename)

    prev.chdir()

def test_is_fastq(tmpdir):
    prev = tmpdir.chdir()
    bad = tmpdir.join('bad.fastq')
    os.symlink(bad.basename, 'good.fastq')

    assert checks.is_fastq('bad.fastq') == problems.PROB_FILE_IS_FASTQ
    assert checks.is_fastq('good.fastq') == problems.PROB_NO_PROBLEM

def test_permission_checker(tmpdir):
    # Create a test file
    p = tmpdir.join("bad_permissions.txt")
    p.write('')
    prev = tmpdir.chdir()

    # Change its permissions a bunch... maybe this is too expensive?
    for m in range(0o300, 0o700, 0o010):
        p.chmod(m)
        prob = checks.has_permission_issues(os.path.abspath(p.basename))
        if not bool(0o040 & m): # octal Unix permission for 'group readable'
            assert prob == problems.PROB_FILE_NOT_GRPRD
        else:
            assert prob == problems.PROB_NO_PROBLEM

    prev.chdir()
