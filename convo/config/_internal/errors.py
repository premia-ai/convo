from .types import Provider


class MissingAiProviderError(Exception):
    def __init__(
        self,
        provider: Provider,
        message="",
    ):
        self.provider = provider
        self.message = (
            message
            or f"'{provider}' hasn't been setup. Hint: Use `convo config set` to do so."
        )
        super().__init__(self.message)
