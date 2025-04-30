class Detector:
    def __init__(self):
        print("AI Detector initialized.")
        self.failed_login_attempts = {}  # Store failed attempts per IP
        self.max_failed_attempts = 3
        self.sensitive_file_attempts = {} # Store access attempts to sensitive files

    def detect(self, activity):
        if "login_attempt" in activity and "incorrect" in activity:
            # Extract the IP address
            parts = activity.split("from ")
            if len(parts) > 1:
                ip_address = parts[1].split(" ")[0]
                if ip_address:
                    self.failed_login_attempts.setdefault(ip_address, 0)
                    self.failed_login_attempts[ip_address] += 1
                    if self.failed_login_attempts[ip_address] >= self.max_failed_attempts:
                        return f"RULE TRIGGERED: Multiple failed logins from {ip_address}"
        elif "command_execution" in activity and "rm -rf /" in activity:
            return "RULE TRIGGERED: Attempt to delete all files!"
        elif "network_scan" in activity and "port 22" in activity:
            return "RULE TRIGGERED: Network scan on SSH port (common attack target)"
        elif "file_access" in activity and "/etc/shadow" in activity:
            parts = activity.split("from ")
            if len(parts) > 1:
                ip_address = parts[1].split(" ")[0]
                self.sensitive_file_attempts.setdefault(ip_address, 0)
                self.sensitive_file_attempts[ip_address] += 1
                if self.sensitive_file_attempts[ip_address] > 2: # More than 2 attempts
                    return f"RULE TRIGGERED: Multiple access attempts to /etc/shadow from {ip_address}"
        elif "login_attempt" in activity and "user:" in activity:
            username_part = [part.strip() for part in activity.split("user:") if part.strip()]
            if username_part:
                username = username_part[0].split(",")[0].strip()
                if username in ["root", "admin"]:
                    return f"RULE TRIGGERED: Login attempt with privileged username: {username}"
        elif "network_scan" in activity and "port" in activity:
            try:
                port = int(activity.split("port ")[1].split(" ")[0])
                if port < 100:
                    parts = activity.split("from ")
                    if len(parts) > 1:
                        ip_address = parts[1].split(" ")[0]
                        return f"RULE TRIGGERED: Network scan on low port ({port}) from {ip_address}"
            except ValueError:
                pass # Handle cases where port parsing fails

        return None

def initialize_detector():
    print("AI Detector initialized.")
    return Detector()