import socket
import json
from pylsl import StreamInfo, StreamOutlet, local_clock

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

# Sesuaikan nama channel sesuai JSON kamu:
# {"t":..., "speed_kmh":..., "brake_input":0/1, "x":..., "y":..., "alt":...}
CHANNELS = ["t", "speed_kmh", "brake_input", "x", "y", "alt"]

info = StreamInfo(
    name="ETS2Telemetry",
    type="Telemetry",
    channel_count=len(CHANNELS),
    nominal_srate=0.0,          # irregular rate (LSL akan timestamp per sample)
    channel_format="float32",   # semua kita kirim sebagai float
    source_id="ets2_telemetry_udp"
)

# (Opsional) isi metadata nama channel
desc = info.desc()
chs = desc.append_child("channels")
for ch in CHANNELS:
    chs.append_child("channel").append_child_value("label", ch).append_child_value("unit", "n/a")

outlet = StreamOutlet(info)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"UDP listening on {UDP_IP}:{UDP_PORT} -> LSL stream '{info.name()}'")

def to_float(v):
    # brake_input biner tetap jadi 0.0/1.0
    try:
        return float(v)
    except Exception:
        return float("nan")

while True:
    data, addr = sock.recvfrom(4096)
    print("RAW UDP bytes from", addr, "len=", len(data))

    s = data.decode("utf-8", errors="ignore")
    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue

        try:
            msg = json.loads(line)
        except Exception as e:
            print("JSON parse failed:", repr(line[:120]), "err:", e)
            continue

        sample = [to_float(msg.get(k)) for k in CHANNELS]
        outlet.push_sample(sample, local_clock())
        print("LSL push:", dict(zip(CHANNELS, sample)))