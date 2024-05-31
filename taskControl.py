from Oficial.run import execute_batch_file
from Oficial.windowControl import hide_window_by_pid, show_window_by_pid
import subprocess

def start_task(bat_file):
    return execute_batch_file(bat_file)

def hide_task(pid):
    hide_window_by_pid(pid)

def show_task(pid):
    show_window_by_pid(pid)

def stop_task(pid):
    subprocess.call(['taskkill', '/f', '/pid', str(pid)])