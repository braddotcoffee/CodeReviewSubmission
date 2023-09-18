from discord import app_commands, Interaction, Client, User

from controllers.sync_controller import SyncController

@app_commands.guild_only()
class SyncCommands(app_commands.Group, name="sync"):
    def __init__(self, tree: app_commands.CommandTree, client: Client) -> None:
            super().__init__()
            self.tree = tree
            self.client = client

    @app_commands.command(name="sync")
    @app_commands.checks.has_role("Mod")
    async def sync(self, interaction: Interaction) -> None:
        """Manually sync slash commands to guild"""
        await SyncController.sync_commands(self.tree, interaction.guild)
        await interaction.response.send_message("Commands synced", ephemeral=True)