import ipyvuetify as v


class DimensionWidget:
    def __init__(self, dimension):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        dimension: int
            The dimension of the dataset
        """

        self.dimension = v.TextField(
            label="Enter the wished dimension (int)",
            type="number",
            outlined=True,
            v_model=dimension,
        )

        self.content = [self.dimension]
