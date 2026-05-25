from pylsl import resolve_stream, StreamInlet

print("Searching for ETS2Telemetry...")
streams = resolve_stream("name", "ETS2Telemetry")
print("Found", len(streams))
inlet = StreamInlet(streams[0])

while True:
    sample, ts = inlet.pull_sample()
    print(ts, sample)