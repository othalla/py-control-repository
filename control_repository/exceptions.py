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


class PuppetfileUpdateException(ControlRepositoryException):
    """
    Puppetfile fails to write content to github
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


class ModuleBadGitReferenceTypeExcption(Exception):
    pass
