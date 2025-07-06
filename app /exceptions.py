class BibleAPIException(Exception):
    """Base exception for Bible API errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class RemoteAPIError(BibleAPIException):
    """Error when communicating with external Bible API"""
    
class DatabaseError(BibleAPIException):
    """Database-related errors"""
    
class VerseNotFoundError(BibleAPIException):
    """When verse is not found locally or remotely"""
    def __init__(self, reference: str):
        super().__init__(
            f"Verse '{reference}' not found",
            status_code=404
        )
