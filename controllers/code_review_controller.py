from typing import Optional

from discord import Interaction
from models.code_review import CodeReview, CodeReviewURL
from db import DB
from db.code_review import CodeReviewDB
from config import YAMLConfig as Config
import re

OWNER_GROUP = 1
REPO_GROUP = 2
BRANCH_GROUP = 3

URL_REGEX = re.compile(r"^(https:\/\/)?github.com\/([\w\-\.]+)\/([\w\-\.]+)(?:\/tree\/(\w+))?\/(pull|commit)\/(\d+|\w+)")
CODE_REVIEW_DB = CodeReviewDB(DB())
CODE_REVIEW_CHANNEL = Config.CONFIG["Discord"]["CodeReview"]["Channel"]
NEEDS_REVIEW_TAG = Config.CONFIG["Discord"]["CodeReview"]["NeedsReviewTag"]


class CodeReviewController:
    @staticmethod
    def validate_url(url: str) -> tuple[bool, Optional[CodeReviewURL]]:
        matches = URL_REGEX.match(url)

        if matches is None:
            return False, None

        capture_groups = matches.groups()
        owner = capture_groups[OWNER_GROUP]
        repo = capture_groups[REPO_GROUP]
        branch = capture_groups[BRANCH_GROUP]
        return True, CodeReviewURL(url, owner, repo, branch)

    @staticmethod
    async def create_review(code_review: CodeReview, interaction: Interaction):
        code_review_channel = interaction.guild.get_channel(CODE_REVIEW_CHANNEL)
        if code_review_channel is None:
            return await interaction.response.send_message(
                f"Failed to submit code review, please try again.", ephemeral=True
            )

        needs_review_tag = code_review_channel.get_tag(NEEDS_REVIEW_TAG)
        _, parsed_url = CodeReviewController.validate_url(code_review.url)
        thread = await code_review_channel.create_thread(
            name=f"{interaction.user.display_name} | {parsed_url.repo} ({code_review.review_type.value})",
            applied_tags=[needs_review_tag],
            content=(
                f"User: {interaction.user.mention}\n"
                f"GitHub Link: {parsed_url.url}\n\n"
                "Description:\n"
                f"{code_review.description}"
            ),
        )
        code_review.message_id = thread.thread.id
        CODE_REVIEW_DB.new_code_review(code_review)

    @staticmethod
    async def create_design(description: str, interaction: Interaction):
        code_review_channel = interaction.guild.get_channel(CODE_REVIEW_CHANNEL)
        if code_review_channel is None:
            return await interaction.response.send_message(
                f"Failed to submit code review, please try again.", ephemeral=True
            )

        needs_review_tag = code_review_channel.get_tag(NEEDS_REVIEW_TAG)
        await code_review_channel.create_thread(
            name=f"{interaction.user.display_name} | (Design Review)",
            applied_tags=[needs_review_tag],
            content=(
                f"User: {interaction.user.mention}\n"
                "Description:\n"
                f"{description}"
            ),
        )