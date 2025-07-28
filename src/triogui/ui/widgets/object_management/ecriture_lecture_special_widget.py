import trioapi as ta
import ipyvuetify as v


class EcritureLectureSpecialWidget:
    def __init__(self, dataset):
        """
        Widget definition to manage Ecriture Lecture Special keyword in the dataset.

        ----------
        Parameters

        dataset: Dataset
            The dataset being modified by the user.

        This widget displays a switch to manage the Ecriture lecture special keyword
        """

        # Store dataset reference
        self.dataset = dataset
        self.type = None

        # Get the value of the keyword Ecriture lecture special if it is in the dataset
        for entry in self.dataset.entries:
            if isinstance(entry, ta.trustify_gen_pyd.Ecriturelecturespecial):
                self.type = entry.type

        # Create a switch based on this value (if user want to write the xyz file then the switch value is true and the keyword is not in the dataset by default)
        self.switch = v.Switch(
            label="Write the xyz file", v_model=None if self.type == "0" else True
        )
        self.switch.observe(self.change_switch, "v_model")

        self.content = [self.switch]

    def change_switch(self, event):
        """
        Update the value of the keyword in the dataset when the switch is changed
        """

        if not self.switch.v_model:
            # Add or change the value of the ecriturelecturespecial keyword
            if self.type is None:
                ta.add_read_object(
                    self.dataset, ta.trustify_gen_pyd.Ecriturelecturespecial(type="0")
                )
                self.type = "0"
            else:
                index = ta.get_entry_index(
                    self.dataset,
                    ta.trustify_gen_pyd.Ecriturelecturespecial(type=self.type),
                )
                self.dataset[index] = ta.trustify_gen_pyd.Ecriturelecturespecial(
                    type="0"
                )
                self.type = "0"
        # Delete the Ecriturelecturespecial keyword
        else:
            ta.delete_read_object(
                self.dataset, ta.trustify_gen_pyd.Ecriturelecturespecial(type=self.type)
            )
