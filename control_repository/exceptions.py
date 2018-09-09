class ControlRepositoryException(Exception):
    """
    Main module exception.
    Also raised when ControlRepository cannot be initialized
    """
    pass


class EnvironmentNotFoundException(ControlRepositoryException):
    """
    Puppet environment not found in the control repository
    """
    pass


class ModuleBadGitReferenceTypeExcption(Exception):
    pass
