import builtins
import traceback

# Save the original print function
original_print = builtins.print


# Define a new print function that includes the stack trace
def custom_print(*args, **kwargs):
    # Avoid calling custom_print recursively by using original_print directly
    original_print(*args, **kwargs)
    # Temporarily restore the original print function for traceback
    builtins.print = original_print
    traceback.print_stack()
    # Restore the custom print function
    builtins.print = custom_print


# Replace the built-in print function with the custom one
builtins.print = custom_print
