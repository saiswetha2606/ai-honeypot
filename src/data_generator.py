def generate_labeled_activity(self):
        activity = random.choice(self.possible_activities)
        log_entry = {"timestamp": time.time()}
        log_entry.update(activity)

        label = "benign"
        if activity["type"] == "login_attempt" and activity["user"] in ["admin", "root"] and activity["result"] == "failure":
            label = "malicious"
        elif activity["type"] == "command_execution" and "rm -rf /" in activity["command"]:
            label = "malicious"
        elif activity["type"] == "file_access" and activity["path"] == "/etc/passwd":
            label = "malicious"
        elif activity["type"] == "network_scan":
            # Randomly select a port from the range
            port = random.choice(activity["port"])
            log_entry["port"] = port  # Update the log entry with the selected port
            if port < 100:
                label = "suspicious"

        log_entry["label"] = label
        return json.dumps(log_entry) + "\n"