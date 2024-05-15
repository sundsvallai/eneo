class NotFoundException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class UnsupportedModelException(Exception):
    pass


class QueryException(Exception):
    pass


class WeaviateException(Exception):
    pass


class UniqueUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


class LoginAuthenticationException(Exception):
    pass


class BadRequestException(Exception):
    pass


class QuotaExceededException(Exception):
    pass


class UniqueException(Exception):
    pass


class OpenAIException(Exception):
    pass


class ValidationException(Exception):
    pass


class PydanticParseError(Exception):
    pass


class NotReadyException(Exception):
    pass


class FileNotSupportedException(Exception):
    pass


class FileTooLargeException(Exception):
    pass


class ChunkEmbeddingMisMatchException(Exception):
    pass


class CrawlerException(Exception):
    pass


# Map exceptions to response codes
# Set message to None to use the internal message
EXCEPTION_MAP = {
    NotFoundException: (404, "Not found"),
    UnauthorizedException: (403, None),
    UnsupportedModelException: (400, None),
    QueryException: (400, None),
    UniqueUserException: (400, None),
    AuthenticationException: (404, "Not found"),
    BadRequestException: (400, None),
    QuotaExceededException: (403, None),
    LoginAuthenticationException: (401, "Unauthenticated"),
    UniqueException: (400, None),
    OpenAIException: (503, None),
    ValidationException: (422, None),
    PydanticParseError: (500, None),
    FileNotSupportedException: (415, None),
    FileTooLargeException: (413, None),
    ChunkEmbeddingMisMatchException: (500, "Something went wrong."),
}
