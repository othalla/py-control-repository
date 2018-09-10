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


class PuppetfileNotFoundException(ControlRepositoryException):
    """
    No Puppetfile in the current environment
    """
    pass


class ModuleParserException(ControlRepositoryException):
    """
    No valid module can be parsed
    """
    pass


class ModuleBadGitReferenceTypeExcption(Exception):
    pass
