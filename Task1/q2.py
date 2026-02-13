# 2. Pass / Fail Analyzer
# Problem Statement:
# Analyze student results.
# marks = [45, 78, 90, 33, 60]

# Requirements:
# A student passes if marks ≥ 50
# Count the total number of pass students
# Count the total number of fail students
# Print the final result clearly
# Real-World Application: Academic evaluation systems
marks = [45, 78, 90, 33, 60]
pass_count = 0
fail_count = 0
for mark in marks:
    if mark >= 50:
        pass_count += 1
    else:
        fail_count += 1
print("Total Students Passed:", pass_count)
print("Total Students Failed:", fail_count)
