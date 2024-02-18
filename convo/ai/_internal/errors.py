class CacheMissError(Exception):
    def __init__(
        self,
        audio_file_path: str,
        message="",
    ):
        self.message = (
            message
            or f"Could not find a cached file matching '{audio_file_path}'. Hint: Have you moved the audio file to a new folder? This breaks the caching mechanism."
        )
        super().__init__(self.message)
