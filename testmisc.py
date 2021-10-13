from traceback import StackSummary
try:
    raise ValueError('Test error')
except ValueError as ve:
    print(ve)