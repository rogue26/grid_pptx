from typing import Union

class GridDesign:
    def __init__(self, layout: Union[list, tuple], contents: Union[list, tuple] = None) -> None:
        self.layout = layout
        self.contents = contents

    def validate_layout(self):
        pass
