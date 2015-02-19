# ditail - Tail directory contents

## Overview

ditail (said "detail") allows you to monitor new lines added to all files in a directory and its subdirectories. Any files added after startup will also be monitored.

ditail operates efficiently in a single thread/process thanks to [asyncio](https://docs.python.org/3/library/asyncio.html) and [pyinotify](https://pypi.python.org/pypi/pyinotify).

### Requirements

- `python>=3.4.2` or (`python >= 3.3` and `asyncio>=3.4.2`)
- `pyinotify>=0.9.5`

[inotify](http://linux.die.net/man/7/inotify) is an API offered only by the Linux kernel, so ditail is limited to Linux-based operating systems.

### Usage

    $ ditail example/

For more information run `ditail -h`.

## Install

### From the PyPI via pip

#### System

    $ pip install ditail

#### Current User only

    $ pip install --user ditail

Ensure `$HOME/.local/bin` is in your shell's `PATH` variable.

### Arch Linux

A PKGBUILD [is available](https://aur.archlinux.org/packages/python-ditail) from the AUR.

## License
The content of this repository is released under the GNU GPL v3.0 or later, as provided in the LICENSE file.

By submitting a "pull request" or otherwise contributing to this repository, you agree to license your contribution under the license mentioned above.
