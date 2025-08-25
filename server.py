import socket
import threading
import time
import xml.etree.ElementTree as ET

HOST = '127.0.0.1'
PORT = 5000

# Read interval and records from XML
def read_xml():
    tree = ET.parse('data.xml')
    root = tree.getroot()
    interval = int(root.find('interval').text)
    records = []
    for rec in root.findall('records/record'):
        speed = rec.find('speed').text
        t = rec.find('time').text
        records.append((speed, t))
    return interval, records

clients = []

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    clients.append(conn)
    try:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"[FROM {addr}] {msg}")
    except:
        pass
    finally:
        clients.remove(conn)
        conn.close()
        print(f"[DISCONNECTED] {addr}")

def start_server():
    interval, records = read_xml()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER STARTED] {HOST}:{PORT}")

    threading.Thread(target=broadcast, args=(interval, records), daemon=True).start()

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

def broadcast(interval, records):
    while True:
        for speed, t in records:
            for c in clients:
                try:
                    c.sendall(f"{speed},{t}\n".encode())
                except:
                    pass
            print(f"[SENT] {speed},{t} | Clients: {len(clients)}")
            time.sleep(interval)

if __name__ == "__main__":
    start_server()
