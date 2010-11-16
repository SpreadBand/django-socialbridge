class BadCredentials(Exception):
    """
    Thrown when a bad credential error happens while trying to use a
    social provider
    """
    pass

class NotAssociatedException(Exception):
    """
    Throw this exception when you need a service to be associated at a
    given point but it's not
    """
    def __init__(self, next_url):
        Exception.__init__(self)
        self.next_url = next_url





