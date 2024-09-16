from robot.libraries.BuiltIn import BuiltIn

class RealTimeListener:
    ROBOT_LISTENER_API_VERSION = 2

    def resolve_argument_value(self, arg):
        """Helper method to resolve variable values."""
        try:
            # Use Robot Framework's BuiltIn library to resolve variable values
            return BuiltIn().replace_variables(arg)
        except:
            # Return the original argument if it cannot be resolved
            return arg

    def format_arguments(self, args):
        """Format arguments for better readability."""
        if not args:
            return None  # Return None if there are no arguments
        return "\n".join([f"  - {self.resolve_argument_value(arg)}" for arg in args])

    def start_keyword(self, name, attrs):
        # Print the keyword name with dash separation based on the level
        formatted_args = self.format_arguments(attrs['args'])  # Format the arguments

        # Print the keyword name
        print(f"\n{attrs['kwname']}")

        # Only print the arguments if they exist
        if formatted_args:
            print(f"Arguments:\n{formatted_args}")

    def end_keyword(self, name, attrs):
        print(f"{attrs['kwname']}\n")
