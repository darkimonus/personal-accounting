class FiltersError(Exception):
    """
    Custom exception for ReceiptsFilterBackend.
    """
    errors: list

    def __init__(self, errors) -> None:
        super().__init__()
        self.errors = errors
