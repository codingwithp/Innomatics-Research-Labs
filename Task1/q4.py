# 4. Message Length Analyzer
# Problem Statement:
# Analyze message sizes.
# messages = ["Hi", "Welcome to the platform", "OK"]

# Requirements:
# Print the length of each message
# Flag messages longer than 10 characters
# Real-World Application: Text filtering and validation systems
message = ["Hi", "Welcome to the platform", "OK"]
for msg in message:
    print(f"Message: '{msg}' Length: {len(msg)}")
    if len(msg) > 10:
        print("-> This message is longer than 10 characters")
