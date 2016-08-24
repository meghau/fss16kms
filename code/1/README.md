# Code Something: Week 1

## Instructions

### Get your Test-Driven Development On.

1. Watch the great [Kent Beck video on how to write a test engine in just a few lines of code](https://www.youtube.com/watch?v=nIonZ6-4nuU). Note
that that example is in CoffeeScript. For the equivalent Python code, see
[utest.py](../src/utest.py).
2. Get the Python equivalent of the watch command used by Beck. Specifically, run the command
   `sudo pip install rerun`
3. Download the `utest.py`
4. Write a python file `main.py` that imports `utest.py` and code from `who1.py who2.py who3.py`;
   i.e. one file per member of your team.
4. Get two windows open:
	 + One editing main.py
	 + One in a shell
5. In the shell, type `rerun "python -B main.py"`
6. Add one more unittest to `main.py`.
     + Important... leave behind at least one failing test.
     + Save the file. Watch the code run.

## Notes

### Video tl;dr:
- It's vital to get feedback. The shorter the feedback loop, the better.
- Coffeescript has `--watch` option that evaulates file every time it's saved. Acts as Self evaluating feedback loop.
- Continues to write a Testing framework to test code. 

### [Rerun package](https://pypi.python.org/pypi/rerun) : Command-line executable Python script to re-run the given command every time files are modified in the current directory or its subdirectories.
	- Usage: `rerun [--help|-h] [--verbose|-v] [--ignore|-i=<file>] [--version] <command>`