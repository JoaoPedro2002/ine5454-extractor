class Parser:
    def __init__(self):
        self._data = None

    def parse(self, id: str):
        raise NotImplementedError("Parser.parse() not implemented")

    def print(self):
        if self._data is None:
            raise Exception("No data to print")
        print(self._data)

    def save_csv(self, path: str):
        if self._data is None:
            raise Exception("No data to save")
        self._data.to_csv(path, index=False)

    def to_json(self):
        if self._data is None:
            raise Exception("No data to save")
        return self._data.to_json(orient="records")