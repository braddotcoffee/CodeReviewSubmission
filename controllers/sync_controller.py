from discord import app_commands, Guild 

class SyncController:
    @staticmethod
    async def sync_commands(tree: app_commands.CommandTree, guild: Guild):
        tree.clear_commands(guild=guild)
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)