class Configuration:
    def __init__(
            self,
            host: str,
            headers: dict = None,
            disable_log: bool = True,
            print_curl: bool = True,
    ):
        self.host = host
        self.headers = headers
        self.disable_log = disable_log
        self.print_curl = print_curl
