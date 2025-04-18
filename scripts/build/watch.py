from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import os
import threading
import time
from .parameters import (
    articles_directory,
    portfolios_directory,
    build_folder__aux_files,
    build_folder__main_output,
    file_types_to_watch,
    watch_frequency_seconds
)
from ..utils.style_console_text import red, green, blue, reset


class MyHandler(FileSystemEventHandler):
    """Class to handle events: creation of new files or modification/deletion of existing ones

    Args:
        FileSystemEventHandler (_type_): _description_
    """
    def __init__(self, trigger_function, trigger_args, file_types):
        super().__init__()
        self.trigger_function = trigger_function
        self.trigger_args = trigger_args
        self.file_types = file_types
        self.lock = threading.Lock()  # 🛡 Lock to prevent re-entry

    def on_modified(self, event):
        self.on_generic( event, f"{blue}Modified{reset}")

    def on_created(self, event):
        self.on_generic(event, f"{green}Created{reset}")

    def on_deleted(self, event):
        self.on_generic(event,f"{red}Deleted{reset}")

    def on_generic(self, event, task:str) -> None:
        if event.src_path.endswith(self.file_types) and not event.is_directory :
            print(event.src_path)
            # ✅ Only run if not already running
            if not self.lock.locked():
                print(f"\n{task}: {event.src_path}")
                threading.Thread(target=self._run_trigger).start()
            # else:
                # print("Trigger function is already running, skipping this event.")


    def _run_trigger(self):
        with self.lock:
            self.trigger_function(self.trigger_args)


def watcher(function_to_trigger, function_arguments, path_to_watch, file_types, frequency_sec) -> None:
    event_handler = MyHandler(function_to_trigger, function_arguments, file_types)
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