from .panel import _GridPanel


class Image(_GridPanel):
    def __init__(self, *args, **kwargs) -> None:
        """

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
