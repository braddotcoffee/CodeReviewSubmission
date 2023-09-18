from discord import app_commands, Interaction, Client, User
from views.submit_review import SubmitReviewModal, DescriptionModal


@app_commands.guild_only()
class CodeReviewCommands(app_commands.Group, name="code_review"):
    def __init__(self, tree: app_commands.CommandTree, client: Client) -> None:
        super().__init__()
        self.tree = tree
        self.client = client

    @app_commands.command()
    async def submit(self, interaction: Interaction):
        """Submit project for code review"""
        await interaction.response.send_modal(SubmitReviewModal())
