import sys
import time


# def progress_bar(iterable, total=None, length=40):
#     total = total or len(iterable)
#     progress = 0
#     for item in iterable:
#         yield item
#         progress += 1
#         percent_complete = progress / total
#         arrow = '=' * int(length * percent_complete)
#         spaces = ' ' * (length - len(arrow))
#         sys.stdout.write(f'\r[{arrow}{spaces}] {int(percent_complete * 100)}%')
#         sys.stdout.flush()
#
#
# # Example usage:
# items = range(1000)
# for item in progress_bar(items):
#     # Simulate some work
#     time.sleep(0.01)
#
# print("\nTask completed!")


# def percentage_bar(iterable, total=None):
#     total = total or len(iterable)
#     progress = 0
#     for item in iterable:
#         yield item
#         progress += 1
#         percent_complete = (progress / total) * 100
#         sys.stdout.write(f'\rProgress: {percent_complete:.2f}%')
#         sys.stdout.flush()
#
# # Example usage:
# items = range(1000)
# for item in percentage_bar(items):
#     # Simulate some work
#     time.sleep(0.01)
#
# print("\nTask completed!")

def static_percentage_bar(percentage, bar_length=20):
    progress = int(bar_length * percentage / 100)
    bar = "[" + "=" * progress + " " * (bar_length - progress) + "]"
    return f"{bar} {percentage:.2f}%"


# Example usage:
completion_percentage = 75.5  # Adjust as needed
bar = static_percentage_bar(completion_percentage)
print(bar)


