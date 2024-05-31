import psutil
import win32gui
import win32process
import win32con
import time

def hide_window_by_pid(pid):
    try:
        # Função de retorno de chamada para encontrar a janela com o PID correspondente
        def callback(hwnd, hwnds):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)

        if not hwnds:
            print("Janela não encontrada.")
            return

        # Oculta a janela
        win32gui.ShowWindow(hwnds[0], win32con.SW_HIDE)

    except Exception as e:
        print("Erro:", e)

def show_window_by_pid(pid):
    try:
        # Função de retorno de chamada para encontrar a janela com o PID correspondente
        def callback(hwnd, hwnds):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)

        if not hwnds:
            print("Janela não encontrada.")
            return

        # Reexibir a janela
        win32gui.ShowWindow(hwnds[0], win32con.SHOW_OPENWINDOW)

    except Exception as e:
        print("Erro:", e)