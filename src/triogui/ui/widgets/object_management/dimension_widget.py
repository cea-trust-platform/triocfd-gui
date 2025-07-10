import ipyvuetify as v
import trioapi as ta


class DimensionWidget:
    def __init__(self, dimension, dataset):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        dimension: int
            The dimension of the dataset
        """
        self.dataset = dataset
        self.dimension = v.TextField(
            label="Enter the wished dimension (int)",
            type="number",
            outlined=True,
            v_model=dimension,
        )
        self.change_dimension_dataset(None)
        self.dimension.observe(self.change_dimension_dataset, "v_model")
        self.content = [self.dimension]

    def change_dimension_dataset(self, change):
        if change:
            ta.change_dimension(self.dataset, int(change["new"]))
