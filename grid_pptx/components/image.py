from .panel import GridPanel


class Image(GridPanel):
    def __init__(self, *args, **kwargs) -> None:
        """

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)