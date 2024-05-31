import psutil

def find_pid_using_port(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return conn.pid
    return None
