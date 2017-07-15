# auto_logger  [![Build Status](https://travis-ci.org/ujiro99/auto_logger.svg?branch=master)](https://travis-ci.org/ujiro99/auto_logger)  [![Coverage Status](https://coveralls.io/repos/github/ujiro99/auto_logger/badge.svg?branch=master)](https://coveralls.io/github/ujiro99/auto_logger?branch=master)

## installation

### how to install non-internet machine.

Download all dependent packages locally.
```sh
$ pip freeze > requirements.txt
$ pip wheel -r requirements.txt -w lib
```

Move all files to non-internet machine, then execute commands below.
```sh
$ pip install -r requirements.txt -f lib --no-index
$ pip install -e .
```
