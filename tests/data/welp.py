class Foo:
    def __init__(self, _: object) -> None:
        self.start = 0

    def __call__(self, **kwds) -> bytes:
        retval = f"Welp{self.start}\n"
        self.start += 1
        return retval.encode()
