from http.server import BaseHTTPRequestHandler, HTTPServer
from Oficial.taskControl import start_task, hide_task, show_task, stop_task
from Oficial.findPidFromPort import find_pid_using_port
import threading
import time

PORT = 6363
BAT_FILE = "C:\\Users\\gusta\\OneDrive\\Documentos\\vs\\teste.bat"  # Substitua pelo caminho do seu arquivo .bat
CHECKTASKS = False

TASKS = {
    "Federate": {"pid": None, "status": "NOT running...", "running": False, "Hidden": True, "port": 9999},
    "Access": {"pid": None, "status": "NOT running...", "running": False, "Hidden": True, "port": 8888},
    "Mock_Intent": {"pid": None, "status": "NOT running...", "running": False, "Hidden": True, "port": 7777},
    "Mock_Token": {"pid": None, "status": "NOT running...", "running": False, "Hidden": True, "port": 6666},
    "Directory": {"pid": None, "status": "NOT running...", "running": False, "Hidden": True, "port": 5555},
    "Redis": {"pid": None, "status": "NOT running...", "running": False, "Hidden": True, "port": 4444}
}

class RequestHandler(BaseHTTPRequestHandler):
        # Inicie o thread para verificar os processos das tarefas

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        with open("Oficial/styles/style.css", "r") as f:
            css_content = f.read()

        with open("Oficial/styles/script.js", "r") as f:
            js_content = f.read()

        response = "<html><head><title>Controle de Tarefa</title>"
        response += f"<style>{css_content}</style>"
        response += f"<script>{js_content}</script>"
        response += "</head><body>"
        response += "<h1>Local Tasks</h1><br/>"
    
        for task in TASKS:
            title_task_len = 11- len(task)
            title_task = f"{task.replace("_", " ")}{'.' * title_task_len}:"
            response += "<div class='task-container'>"  # Abre a div task-container
            # Botões de controle
            response += "<form method='post' style='display: flex; justify-content: flex-start; margin-top: 20px;'>"
            response += f"<span class='task-title' style='align-content: center; font-size: 24; font-family: monospace; margin-left: 50'>{title_task}</span>"
            if TASKS[task]["running"]:
                response += f"<input type='submit' name='{task}stop' value='Encerrar' onclick=\"reloadPage()\">"
                if TASKS[task]["Hidden"]:
                    response += f"<input type='submit' name='{task}show' value='Mostrar' onclick=\"reloadPage()\">"
                else:
                    response += f"<input type='submit' name='{task}hide' value='Ocultar' onclick=\"reloadPage()\">"
            else:
                response += f"<input type='submit' name='{task}start' value='Iniciar' onclick=\"reloadPage()\">"

            response += "</form></div>"  # Fecha a div task-container

        response += "</body></html>"
        
        self.wfile.write(response.encode())


    def do_POST(self):
        global CHECKTASKS
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        print(f"POST: {post_data}")
        task = self.get_Task(post_data)
        
        if task in TASKS and ('start' in post_data or TASKS[task]["pid"]):
            if 'start' in post_data:
                TASKS[task]["pid"] = start_task(BAT_FILE)
                TASKS[task]["running"] = True
                TASKS[task]["Hidden"] = True
            elif 'hide' in post_data:
                hide_task(TASKS[task]["pid"])
                TASKS[task]["Hidden"] = True
            elif 'show' in post_data:
                show_task(TASKS[task]["pid"])
                TASKS[task]["Hidden"] = False
            elif 'stop' in post_data:
                stop_task(TASKS[task]["pid"])
                TASKS[task]["running"] = False
        
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

        if not CHECKTASKS:
            task_checker_thread = threading.Thread(target=self.check_tasks, args=(self))
            task_checker_thread.start()
            CHECKTASKS = True

    def get_Task(self, post_data):
        currentTask = None
        for task in TASKS:
            if task in post_data:
                currentTask = task
                break
        return currentTask
    
    def check_tasks(self):
        while True:
            print("entrou")
            time.sleep(10)
            reloadPage = False
            for task in TASKS:
                pid_port = find_pid_using_port(TASKS[task]["port"])
                if pid_port != TASKS[task]["pid"]:
                    reloadPage = True
                    if TASKS[task]["pid"]:
                        stop_task(TASKS[task]["pid"])
                    
                    if pid_port:
                        TASKS[task]["running"] = True
                        if TASKS[task]["Hidden"]:
                            show_task(pid_port)
                    else:
                        TASKS[task]["running"] = False
                        TASKS[task]["Hidden"] = True
                    
                    TASKS[task]["pid"] = pid_port

            print(f"reload: {reloadPage}")
            if reloadPage:
                self.send_response(303)
                self.send_header("Location", "/")
                self.end_headers()

    def reload_page(self):
        pass

try:
    server = HTTPServer(("localhost", PORT), RequestHandler)
    print(f"Servidor rodando em http://localhost:{PORT}/")
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServidor parado.")
