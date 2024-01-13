from discord import app_commands, Interaction, Client
from views.submit_design import SubmitDesignReviewModal
from views.submit_review import SubmitReviewModal


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

    @app_commands.command()
    async def design(self, interaction: Interaction):
        """Submit for assistance in designing your next feature!"""
        await interaction.response.send_modal(SubmitDesignReviewModal())