from httpx import Response


class KrakenResponse:
    def __init__(self, response: Response):
        self.error: list[str] = response.json()['error']
        self.isError: bool = True if self.error else False