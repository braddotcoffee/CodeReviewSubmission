from discord import Color, Embed, app_commands, Interaction, Client, User
from config import YAMLConfig as Config

from controllers.sync_controller import SyncController

MODERATOR_ROLE = Config.CONFIG["Discord"]["ModeratorRole"]


@app_commands.guild_only()
class SyncCommands(app_commands.Group, name="sync"):
    def __init__(self, tree: app_commands.CommandTree, client: Client) -> None:
        super().__init__()
        self.tree = tree
        self.client = client

    @app_commands.command(name="sync")
    @app_commands.checks.has_role(MODERATOR_ROLE)
    async def sync(self, interaction: Interaction) -> None:
        """Manually sync slash commands to guild"""
        await SyncController.sync_commands(self.tree, interaction.guild)
        await interaction.response.send_message("Commands synced", ephemeral=True)

    @app_commands.command()
    @app_commands.checks.has_role(MODERATOR_ROLE)
    async def dump_tags(self, interaction: Interaction) -> None:
        """Dump tags applied to a forum post"""
        tag_names = []
        tag_ids = []
        for tag in interaction.channel.applied_tags:
            tag_names.append(tag.name)
            tag_ids.append(str(tag.id))
        embed = Embed(
            title="Tags Dump",
            description="Tags applied to this post",
            color=Color.green()
        )
        embed.add_field(name="Name", value="\n".join(tag_names))
        embed.add_field(name="ID", value="\n".join(tag_ids), inline=True)
        await interaction.response.send_message(embed=embed)
        