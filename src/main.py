from src.listener import start_listener
from src.detector import initialize_detector
from src.utils import log_activity

def main():
    print("Starting the AI Honeypot...")

    # Initialize components
    listener = start_listener()
    detector = initialize_detector()

    # Main loop to listen and detect (this is a placeholder)
    try:
        while True:
            activity = listener.listen()  # Simulate listening
            if activity:
                log_activity(f"Activity detected: {activity}")
                prediction = detector.detect(activity)
                if prediction:
                    log_activity(f"Potential malicious activity detected: {prediction}")
    except KeyboardInterrupt:
        print("Honeypot stopped.")

if __name__ == "__main__":
    main()