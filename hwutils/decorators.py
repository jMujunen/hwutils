def auto_repr(cls):
    cls.__repr__ = (
        lambda self: f"{self.__class__.__name__}({', '.join(f'{k}={getattr(self, k)}' for k in self.__dict__.keys())})"
    )
    return cls
