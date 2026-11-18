import psutil, time

def find_node_processes():
    nodes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        name = proc.info['name'] or ''
        cmdline = proc.info['cmdline'] or []
        if name == 'python.exe' and any('app.py' in part for part in cmdline):
            nodes.append(proc)
    return nodes

nodes = find_node_processes()
print("发现节点主进程：", [proc.pid for proc in nodes])

# 第一次调用cpu_percent() 只是建立基线，必须先调用一次再丢弃
for proc in nodes:
    proc.cpu_percent(interval=None)

while True:
    time.sleep(1)
    for p in list(nodes):        
        try:
            children = p.children(recursive=True)
            print(p.pid, "main", p.cpu_percent(), "| workers:",
                  [(c.pid, c.cpu_percent()) for c in children])
        except psutil.NoSuchProcess:
            print(p.pid, "已退出")
            nodes.remove(p)