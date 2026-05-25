import socket, json
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5005))
print("listening 0.0.0.0:5005")
while True:
    data, _ = sock.recvfrom(4096)
    s = data.decode("utf-8", errors="ignore").strip()
    if s:
        print(json.loads(s))