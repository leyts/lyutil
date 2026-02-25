"""Custom exceptions for lyutil."""


class InvalidPathError(ValueError):
    """Raised when a path has no usable stem."""


class TimestampParseError(ValueError):
    """Raised when a filename does not contain a valid timestamp."""
