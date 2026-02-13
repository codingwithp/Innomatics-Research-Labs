# 1. User Login Check
# Problem Statement:
# Given a username and password, check whether login is successful.
# username = "admin"
# password = "1234"

# Requirements:
# Print "Login Successful" if both username and password match
# Otherwise print "Invalid Credentials"
# Real-World Application: Authentication system


input_username = input("Enter username: ")
input_password = input("Enter password: ")
if input_username =="admin" and input_password == "1234":
    print("Login Successful")
else:
    print("Invalid Credentials")
