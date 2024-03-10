from shopping import app, config

PORT = config.Config.PORT

# Compare this snippet from shopping/__init__.py:
if __name__ == "__main__":
    """
    If the next error occurs:
    socket.error: [Errno 10013] An attempt was made to access a socket in a way forbidden by its access permissions
    then, put the port number to some other value than 5000, for example 8000. Port can be get from .env file or
    from the configuration file.
    """
    app.run(
        debug=True, port=PORT
    )  # Run the app in debug mode (for development purposes only!)
