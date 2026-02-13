# 5. Error Message Detector
# Problem Statement:
# Detect error messages from system logs.
# logs = ["INFO", "ERROR", "WARNING", "ERROR"]

# Requirements:
# Count the number of "ERROR" entries
logs = ["INFO", "ERROR", "WARNING", "ERROR"]
error_count = logs.count("ERROR")
print("Number of ERROR entries:", error_count)
