

class ProviderException(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__()
        self.inner = args[0]

    def __str__(self) -> str:
        return "| {0} Inner Error: {1}".format(super().__str__(), self.inner)