class CustomException(Exception):
    """ログイン時エラー"""

    def __init__(self, *message):
        super().__init__(message)