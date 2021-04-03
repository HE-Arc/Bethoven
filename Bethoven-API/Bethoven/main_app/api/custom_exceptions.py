from rest_framework.exceptions import APIException
class UserUpdateError(APIException):
    """Readers error class"""
    def init(self, msg):
        APIException.init(self, msg)
        self.message = msg