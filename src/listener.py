import random
import time

class Listener:
    def __init__(self):
        print("Listener initialized.")

    def listen(self):
        time.sleep(random.uniform(0.5, 2))

        if random.random() < 0.5:  # Increase chance of specific activity for testing
            activity_type = "network_scan"
            ip_address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            port = 22  # Force the port to 22
            return f"[{activity_type}] Network scan detected from {ip_address} on port {port}"
        elif random.random() < 0.7: # Keep some other activity for variety
            activity_type = random.choice(["login_attempt", "file_access", "command_execution"])
            ip_address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            if activity_type == "login_attempt":
                username = random.choice(["guest", "user"])
                password = "incorrect"
                return f"[{activity_type}] Attempt from {ip_address} with user: {username}, pass: {password}"
            elif activity_type == "file_access":
                file_path = random.choice(["/tmp/test.txt"])
                return f"[{activity_type}] Access to file: {file_path} from {ip_address}"
            elif activity_type == "command_execution":
                command = random.choice(["ls", "pwd"])
                return f"[{activity_type}] Command executed: '{command}' by {ip_address}"
        return None

def start_listener():
    print("Start listener function called")
    return Listener()