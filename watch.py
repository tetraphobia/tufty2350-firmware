#!/usr/bin/env python3
import subprocess
import time
import threading
import argparse

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

parser = argparse.ArgumentParser(prog="tuftywatcher")
parser.add_argument("--serial", help="Serial port to connect to", default="/dev/ttyACM0")
parser.add_argument("--script", help="Python script to run on file change", default="main.py")


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, serial, script):
        self.last_run = 0
        self.serial = serial
        self.script = script
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
        subprocess.run(['mpremote', self.serial, 'reset'], capture_output=True, text=True)

        print("Running script...")
        self.current_process = subprocess.Popen(['mpremote', 'connect', self.serial, 'run', self.script])

if __name__ == "__main__":
    args = parser.parse_args()
    handler = ReloadHandler(args.serial, args.script)
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
