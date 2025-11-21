import mss

try:
    with mss.mss() as sct:
        print("Monitors:", sct.monitors)
        # Try capturing the first monitor
        sct.grab(sct.monitors[1])
        print("Capture successful!")
except Exception as e:
    print(f"MSS Failed: {e}")
