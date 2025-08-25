import socket

HOST = '127.0.0.1'
PORT = 5000

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("[CONNECTED TO SERVER]")

    buffer = ""

    try:
        while True:
            data = client.recv(1024).decode()
            if not data:
                break
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if line:
                    speed_str, t = line.split(',')
                    speed = int(speed_str)
                    print(f"Received: Speed={speed} km/h, Time={t}")

                    # W1 warning: speed between 80 and 110 
                    if 80 <= speed <= 110:
                        print("W1: Speed is between 80 and 110 km/h")
                        client.sendall(b"W1\n")

                    # W2 warning: speed >= 120
                    if speed >= 120:
                        print("W2: Speed is greater than 120 km/h")
                        client.sendall(b"W2\n")

    except KeyboardInterrupt:
        print("Client closed.")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
