class NoPwdAlertException:
  """自定义异常类"""

    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

    def __str__(self):
        return f"CustomException: {self.args[0]}"