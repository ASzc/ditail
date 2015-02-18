#!/usr/bin/env python3

import argparse
import asyncio
import logging
import os
import sys

import pyinotify

logger = logging.getLogger("dtail")

@asyncio.coroutine
def tail_task(path, loop, new=False):
    cmd = ["tail", "-fq", "--pid", str(os.getpid()), "-n"]
    if new:
        cmd.append("+1")
    else:
        cmd.append("0")
    cmd.append(path)
    proc = yield from asyncio.create_subprocess_exec(*cmd, loop=loop, stdout=asyncio.subprocess.PIPE)
    try:
        line = yield from proc.stdout.readline()
        while line:
            sys.stdout.write(line)
            line = yield from proc.stdout.readline()
    finally:
        proc.terminate()

def update_tasks_in(directory, tail_tasks, loop):
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE

    class Handler(pyinotify.ProcessEvent):
        def process_IN_CREATE(self, event):
            path = event.pathname
            if os.path.isfile(path):
                if path in tail_tasks:
                    logger.debug("Cancelling existing task for {}".format(path))
                    tail_tasks[path].cancel()
                    del tail_tasks[path]
                logger.debug("Creating task for {}".format(path))
                tail_tasks[path] = loop.create_task(tail_task(path, loop, new=True))
            else:
                logger.debug("New path {} is not a file, ignoring".format(path))

        def process_IN_DELETE(self, event):
            path = event.pathname
            if path in tail_tasks:
                logger.debug("Cancelling task for {}".format(path))
                tail_tasks[path].cancel()
                del tail_tasks[path]
            else:
                logger.debug("No task to cancel for {}".format(path))

    notifier = pyinotify.AsyncioNotifier(wm, loop, default_proc_fun=Handler())
    wm.add_watch(directory, mask, rec=True, auto_add=True)

def generate_files_in(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

def tail_files_in(directory):
    loop = asyncio.get_event_loop()
    tail_tasks = dict()
    abs_directory = os.path.abspath(directory)

    try:
        for path in generate_files_in(abs_directory):
            logger.debug("Creating initial task for {}".format(path))
            tail_tasks[path] = loop.create_task(tail_task(path, loop))
        update_tasks_in(abs_directory, tail_tasks, loop)

        logger.debug("Starting loop")
        loop.run_forever()
        logger.debug("Loop stopped")
    except KeyboardInterrupt:
        loop.stop()
        logger.debug("Keyboard Interrupt, loop stopped")
    finally:
        for task in tail_tasks.values():
            task.cancel()

#
# Main
#

def create_argparser():
    parser = argparse.ArgumentParser(description="Prints any new lines added to all files in a directory tree, inotify is used for new/deleted file awareness.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable logging (at DEBUG level)")
    parser.add_argument("directory", help="The directory to look in for files to tail")
    return parser

def setup_logging():
    logging.basicConfig(level=logging.DEBUG)

def configure_stdio():
    sys.stdout = os.fdopen(sys.stdout.fileno(), "wb", buffering=0)

def main():
    parser = create_argparser()
    args = parser.parse_args()
    if args.debug:
        setup_logging()
    configure_stdio()
    tail_files_in(args.directory)

if __name__ == "__main__":
    main()
