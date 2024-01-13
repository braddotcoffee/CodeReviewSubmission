
from discord import TextStyle
from discord.interactions import Interaction
from discord.ui import Modal, TextInput

from controllers.code_review_controller import CodeReviewController

class SubmitDesignReviewModal(Modal, title="Submit your design for review!"):
    def __init__(self):
        super().__init__(timeout=None)
        self.title = f"Tell me about your feature"
        self.i_accept_text = f"I accept"

        self.description = TextInput(
            label="What should I know about your feature?",
            style=TextStyle.paragraph,
            min_length=20,
            required=True,
        )

        self.i_accept = TextInput(
            label=f"Your feature idea will be shown on stream",
            placeholder=self.i_accept_text,
            min_length=len(self.i_accept_text),
            max_length=len(self.i_accept_text),
        )

        self.add_item(self.i_accept)
        self.add_item(self.description)

    async def on_submit(self, interaction: Interaction):
        if self.i_accept.value.lower() != self.i_accept_text.lower():
            return await interaction.response.send_message(
                "You must accept that your GitHub will be shown on stream to submit code for review",
                ephemeral=True,
            )

        await CodeReviewController.create_design(self.description.value, interaction)
        await interaction.response.send_message("Successfully created design review!", ephemeral=True)
