from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import os
import threading
import time
from pathlib import Path
from scripts.utils.style_console_text import red, green, blue, reset
import argparse
from typing import Callable

class MyHandler(FileSystemEventHandler):
    """Class to handle events: creation of new files or modification/deletion of existing ones

    Args:
        FileSystemEventHandler (_type_): _description_
    """
    def __init__(self, trigger_function, trigger_args, file_types, paths_to_ignore):
        super().__init__()
        self.trigger_function = trigger_function
        self.trigger_args = trigger_args
        self.file_types = file_types
        self.paths_to_ignore = paths_to_ignore
        self.lock = threading.Lock()  # 🛡 Lock to prevent re-entry

    def on_modified(self, event):
        self.on_generic( event, f"{blue}Modified{reset}")

    def on_created(self, event):
        self.on_generic(event, f"{green}Created{reset}")

    def on_deleted(self, event):
        self.on_generic(event,f"{red}Deleted{reset}")


    def on_generic(self, event, task:str) -> None:
        file_path = event.src_path

        if (
            file_path.endswith(self.file_types) # check if file is of one of the targetted file types
            and not event.is_directory # check if changed path is actually a directory, not a file
            and not any(p in file_path for p in self.paths_to_ignore) # check if file is excluded or part of an excluded folder
        ):
            # ✅ Only run if not already running
            if not self.lock.locked():
                print(f"\n{task}: {file_path}")
                threading.Thread(target=self._run_trigger).start()
            # else:
                # print("Trigger function is already running, skipping this event.")


    def _run_trigger(self):
        with self.lock:
            self.trigger_function(self.trigger_args)


def watcher(function_to_trigger:Callable, function_arguments:argparse.Namespace, path_to_watch:str, file_types : tuple[str, ...], paths_to_ignore:  list[str] , frequency_sec: int) -> None:
    """ watcher to detect creation of new files, or deletion/changes of existing ones, and trigger a desired behavior.

    Args:
        function_to_trigger (function): function to trigger on changes
        function_arguments (argparse.Namespace): arguments that are passed to the function
        path_to_watch (str): path to watch recursively
        file_types (tuple[str, ...]): tuple of file types to watch, to the exclusion of others
        paths_to_ignore (list[str]): list of paths to be ignored by watcher, be them files on folders
        frequency_sec (int): frequency at which the watcher is triggered
    """
    event_handler = MyHandler(function_to_trigger, function_arguments, file_types, paths_to_ignore)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch,
                      recursive=True # to watch subfolders
                      )
    observer.start()


    try:
        # trigger on start
        function_to_trigger(function_arguments)
        # and then watch for changes
        while True:
            # time.sleep(frequency_sec)
            slow_type("...", frequency_sec)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



def slow_type(text:str, frequency_sec:int) -> None:
    """Gradually print out a string in the console

    Args:
        text (str): string to print to console
        frequency_sec (int): speed in seconds that the whole string takes to print
    """
    for l in text:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(frequency_sec/len(text))
    print("")