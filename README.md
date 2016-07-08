# BotBot
[![Build Status](https://travis-ci.org/jackstanek/BotBot.svg?branch=master)](https://travis-ci.org/jackstanek/BotBot)
[![Coverage Status](https://coveralls.io/repos/github/jackstanek/BotBot/badge.svg?branch=master)](https://coveralls.io/github/jackstanek/BotBot?branch=master)

A manager for lab computational resources.

# Functionality

- Ensures all files in a shared folder are group readable.
- Encourages users to use symbolic links instead of copying large
  files.
- Suggests file compression when appropriate to save space.
- Modular design allowing for easy extension.

# Installation

## Manual

If you want the latest and greatest development code, go ahead and
clone this repo:

```
git clone https://github.com/jackstanek/BotBot.git
cd BotBot
```

then run

```
pip install -r requirements.txt
```

If you want to run the test suite as well, you'll need to run

```
pip install -r test_requirements.txt
```

To run the test suite just run `py.test` in the project directory.

# Configuration

BotBot uses 2 primary configuration files: `~/.botbotignore` and
`~/.botbot/botbot.conf`.

## `.botbotignore`

This is a list of files that BotBot won't check. It is similar in
structure to a `.gitignore` file, but it's a bit simpler. Instead of
git's structure, each line is a string which can be handled by the
Python built-in [`glob`](https://docs.python.org/3/library/glob.html)
module. Anything after a `#` character will be ignored, so these can
be used to add comments.

## `.botbot/botbot.conf`

Configuration variables are stored here. The file is an .ini-style
configuration formatted file. The variables are stored in sections as
follows:

- `[checks]`
    - `oldage`: defines how many days old a file must be to be
      considered "old".

    - `largesize`: defines how many bytes large a file must be to be
      considered "large".

- `[fileinfo]`
    - `important`: defines which file extensions are considered
      "important." By default, *.sam and *.bam files are denoted as
      important.

- `[email]` <span style='font-size: 0.5em'><span style='color: red'>*</span>(REQUIRED for email mode)</span>
    - `domain`: the domain that the users' email accounts are on
    - `email`: your email address (which emails are sent from)
    - `password`: your email password
    - `smtp_server`: the SMTP server you will send from
    - `smtp_port`: the port the SMTP server uses (probably 587, check
      with your server administrator or documentation)

# Testing

BotBot uses pytest as its test suite. To run the tests, run
```py.test``` in the project root directory.
