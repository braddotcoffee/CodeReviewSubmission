from discord import TextStyle
from discord.interactions import Interaction
from discord.ui import Modal, TextInput
from controllers.code_review_controller import CodeReviewController
from models.code_review import CodeReviewType, CodeReview
import logging

LOG = logging.getLogger(__name__)


class SubmitReviewModal(Modal, title="Submit your project for code review!"):
    def __init__(self):
        super().__init__(timeout=None)
        self.url = TextInput(label="Link to your pull request (github.com)")
        self.title = f"Tell me about your repo"
        self.i_accept_text = f"I accept"

        self.description = TextInput(
            label="What should I know about your project?",
            style=TextStyle.paragraph,
            min_length=20,
            max_length=1000,
            required=True,
        )

        self.i_accept = TextInput(
            label=f"Your GitHub username will be shown on stream",
            placeholder=self.i_accept_text,
            min_length=len(self.i_accept_text),
            max_length=len(self.i_accept_text),
        )

        self.add_item(self.url)
        self.add_item(self.i_accept)
        self.add_item(self.description)

    async def on_submit(self, interaction: Interaction):
        provided_url = self.url.value
        valid, parsed_url = CodeReviewController.validate_url(provided_url)
        if not valid:
            await interaction.response.send_message(
                "Invalid project URL provided - only GitHub PR links accepted",
                ephemeral=True,
            )

        if self.i_accept.value.lower() != self.i_accept_text.lower():
            return await interaction.response.send_message(
                "You must accept that your GitHub will be shown on stream to submit code for review",
                ephemeral=True,
            )

        code_review = CodeReview(
            guild_id=interaction.guild_id,
            message_id=None,
            user_id=interaction.user.id,
            description=self.description.value,
            url=parsed_url.url,
            review_type=CodeReviewType.general,
        )
        await CodeReviewController.create_review(code_review, interaction)
        await interaction.response.send_message("Successfully created code review!")
