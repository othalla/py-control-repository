class ControlRepositoryException(Exception):
    """
    Main module exception.
    Also raised when ControlRepository cannot be initialized
    """
    pass


class ModuleMalformedException(Exception):
    """
    When a module is called without correct params
    A GitModule with a github reference type but no reference
    """
    pass


class EnvironmentNotFoundException(ControlRepositoryException):
    """
    Puppet environment not found in the control repository
    """
    pass


class ModuleNotFoundException(ControlRepositoryException):
    """
    Module not found in Puppetfile
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


class ModuleAlreadyPresentException(ControlRepositoryException):
    """
    When a puppet module is already present in some puppetfile
    """
    pass
