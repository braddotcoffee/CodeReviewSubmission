from discord import ButtonStyle, TextStyle, SelectOption
from discord.interactions import Interaction
from discord.ui import Modal, Select, View, Button, TextInput
from controllers.code_review_controller import CodeReviewController
from models.code_review import CodeReviewURL, CodeReviewType, CodeReview
import logging

LOG = logging.getLogger(__name__)
USERNAME_MAX_LENGTH = 20


class SubmitReviewModal(Modal, title="Submit your project for code review!"):
    url = TextInput(label="Link to your project (github.com)")

    async def on_submit(self, interaction: Interaction):
        provided_url = self.url.value
        valid, parsed_url = CodeReviewController.validate_url(provided_url)
        if not valid:
            await interaction.response.send_message(
                "Invalid project URL provided - only GitHub links accepted",
                ephemeral=True,
            )

        await interaction.response.send_message(
            view=ProjectDetailsView(parsed_url), ephemeral=True
        )


class DescriptionModal(Modal, title="Temp"):
    def __init__(self, parsed_url: CodeReviewURL, review_type: CodeReviewType):
        super().__init__(timeout=None)
        self.parsed_url = parsed_url
        self.review_type = review_type
        self.title = f"Tell me about {parsed_url.repo}"
        self.i_accept_text = "I accept"

        self.description = TextInput(
            label="What should I know about your project?",
            style=TextStyle.paragraph,
            min_length=20,
            max_length=1000,
            required=True,
        )
        username = self.parsed_url.owner
        if len(username) > USERNAME_MAX_LENGTH:
            username = username[: USERNAME_MAX_LENGTH - 3] + "..."

        self.i_accept = TextInput(
            label=f"{username} will be shown on stream",
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

        code_review = CodeReview(
            guild_id=interaction.guild_id,
            message_id=None,
            user_id=interaction.user.id,
            description=self.description.value,
            url=self.parsed_url.url,
            review_type=self.review_type,
        )
        await CodeReviewController.create_review(code_review, interaction)


class ProjectDetailsView(View):
    def __init__(self, parsed_url: str):
        super().__init__(timeout=None)

        self.parsed_url = parsed_url

        options = [
            SelectOption(
                label="I want general feedback on code structure / approach",
                value=CodeReviewType.general.value,
            ),
            SelectOption(
                label="I have a specific question (include in description)",
                value=CodeReviewType.specific_question.value,
            ),
            SelectOption(
                label="I have a bug I'd like help finding (experimental)",
                value=CodeReviewType.bug.value,
            ),
        ]

        self.review_type = Select(
            placeholder="What do you want to get out of this review?", options=options
        )

        self.add_item(self.review_type)

    async def interaction_check(self, interaction: Interaction) -> bool:
        await interaction.response.send_modal(
            DescriptionModal(
                self.parsed_url, CodeReviewType[self.review_type.values[0]]
            )
        )
