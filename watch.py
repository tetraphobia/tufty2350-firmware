#!/usr/bin/env python3
import subprocess
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_run = 0
        self.current_process = None

    def on_modified(self, event):
        if not event.src_path.endswith('.py'):
            return
        now = time.time()
        if now - self.last_run < 1:
            return
        self.last_run = now
        print(f"Change detected in {event.src_path}")
        threading.Thread(target=self.reload).start()

    def reload(self):
        if self.current_process is not None:
            print("Killing previous process...")
            self.current_process.kill()
            self.current_process.wait()
            self.current_process = None

        print("Resetting device...")
        subprocess.run(['mpremote', 'a0', 'reset'], capture_output=True, text=True)

        print("Running script...")
        self.current_process = subprocess.Popen(['mpremote', 'a0', 'run', 'firmware/apps/badge/__init__.py'])

if __name__ == "__main__":
    handler = ReloadHandler()
    observer = Observer()
    observer.schedule(handler, path='.', recursive=True)
    observer.start()
    print("Watching for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
