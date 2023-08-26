# Singleton allows creating only one instance of the class and provides a global access point to this instance,
# to avoid AttributeError
class Singleton:
    def __new__(cls, *args, **kwargs):
        # Handles the process of creating an instance of the class
        if not hasattr(cls, 'instance'):
            # Check if the 'instance' attribute exists in the class 'cls'.
            # If it doesn't exist, it means an instance of the class hasn't been created yet.
            cls.instance = super(Singleton, cls).__new__(cls)
            # Create a new instance of the class
        return cls.instance
        # Returns the instance of the class
