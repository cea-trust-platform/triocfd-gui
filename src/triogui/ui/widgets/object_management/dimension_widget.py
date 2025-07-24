import ipyvuetify as v
import trioapi as ta


class DimensionWidget:
    def __init__(self, dimension, dataset):
        """
        Widget definition to manage the dimension value of the dataset.

        ----------
        Parameters

        dimension: int
            The current dimension of the dataset.

        dataset: Dataset
            The dataset whose dimension is being modified.

        This widget provides a numeric input field for setting the dataset's dimension.
        Any change in the value immediately updates the dataset via the Trio API.
        """

        # Store dataset reference
        self.dataset = dataset

        # Create a text field (number input) for the dimension value
        self.dimension = v.TextField(
            label="Enter the wished dimension (int)",
            type="number",
            outlined=True,
            v_model=dimension,
        )

        # Initialize the dataset with the given dimension
        self.change_dimension_dataset(None)

        # Observe changes to the input field and update the dataset
        self.dimension.observe(self.change_dimension_dataset, "v_model")

        # Store UI content
        self.content = [self.dimension]

    def change_dimension_dataset(self, change):
        """
        Called when the dimension input value is changed.

        Updates the dimension value in the dataset using the Trio API.
        """
        if change:
            ta.change_dimension(self.dataset, int(change["new"]))
