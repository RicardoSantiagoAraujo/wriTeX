from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
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


class MyHandler(FileSystemEventHandler):
    def __init__(self, trigger_function, trigger_args, file_types):
        super().__init__()
        self.trigger_function = trigger_function
        self.trigger_args = trigger_args
        self.file_types = file_types
        self.lock = threading.Lock()  # 🛡 Lock to prevent re-entry

    def on_modified(self, event):
        if event.src_path.endswith(self.file_types) and not event.is_directory :
            # ✅ Only run if not already running
            if not self.lock.locked():
                print(f"Modified: {event.src_path}")
                threading.Thread(target=self._run_trigger).start()
            # else:
                # print("Trigger function is already running, skipping this event.")


    def on_created(self, event):
        if event.src_path.endswith(self.file_types) and not event.is_directory :
            # ✅ Only run if not already running
            if not self.lock.locked():
                print(f"Created: {event.src_path}")
                threading.Thread(target=self._run_trigger).start()
            # else:
                # print("Trigger function is already running, skipping this event.")


    def on_deleted(self, event):
        if event.src_path.endswith(self.file_types) and not event.is_directory :
            # ✅ Only run if not already running
            if not self.lock.locked():
                print(f"Deleted: {event.src_path}")
                threading.Thread(target=self._run_trigger).start()
            # else:
                # print("Trigger function is already running, skipping this event.")


    def _run_trigger(self):
        with self.lock:
            self.trigger_function(self.trigger_args)


def watcher(function_to_trigger, function_arguments, path_to_watch, file_types, frequency_sec):
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
            time.sleep(frequency_sec)
            # function_to_trigger(function_arguments)
            print("...")
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
