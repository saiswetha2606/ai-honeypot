import time
from src.listener import start_listener # You might adapt this to use DataGenerator
from src.detector import initialize_detector
from src.utils import setup_logger
import logging

logger = setup_logger('honeypot', 'honeypot.log')

def main():
    logger.info("Starting the AI Honeypot...")
    listener = start_listener() # Or your data generation mechanism
    detector = initialize_detector()

    while True:
        activity = listener.listen()
        if activity:
            logger.info(f"Raw activity: {activity}")
            detection_result = detector.detect(activity)
            if detection_result:
                logger.warning(f"Potential malicious activity detected: {detection_result}")
        time.sleep(1)

if __name__ == "__main__":
    main()