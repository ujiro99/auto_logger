# auto_logger  [![Build Status](https://travis-ci.org/ujiro99/auto_logger.svg?branch=master)](https://travis-ci.org/ujiro99/auto_logger)  [![Coverage Status](https://coveralls.io/repos/github/ujiro99/auto_logger/badge.svg?branch=master)](https://coveralls.io/github/ujiro99/auto_logger?branch=master)

## Usage

```
Usage: mlog [OPTIONS] COMMAND [ARGS]...

  If subcommand is omitted, start is executed.

Options:
  -t, --test-number TEXT  Directory name to save the log.
  --debug / --no-debug    Output debug logs.
  --help                  Show this message and exit.

Commands:
  clear    Delete all log files saved in Remote.
  convert  Extracts the specified tar file and converts it according to conversion rules.
  get      Get the file specified as an argument. If omitted, it will be newly acquired.
  init     Set parameters to be used for log acquisition. The setting value is saved in ~ / plog.ini.
  ls       Get a list of log files saved in Remote.
  start    Start collecting logs including console operation log. To exit the log acquisition, please input `exit` twice.
```

## Installation

### how to install non-internet machine.

Download all dependent packages locally.
```sh
$ pip wheel -r requirements.txt -w lib
```

Move all files to non-internet machine, then execute commands below.
```sh
$ sudo pip install -r requirements.txt -f lib --no-index
$ sudo pip install -e . -f lib --no-index
```
