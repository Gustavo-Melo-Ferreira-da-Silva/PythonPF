import subprocess
import psutil
import time

def execute_batch_file(file_path):
    # Executa o arquivo batch em uma nova janela de console
    process = subprocess.Popen(file_path, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    return process.pid
