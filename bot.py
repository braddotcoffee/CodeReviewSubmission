import asyncio
import discord
from discord import Client, Guild, Intents, app_commands
from commands.code_review import CodeReviewCommands
from commands.sync import SyncCommands
from controllers.sync_controller import SyncController
from db import DB
from config import YAMLConfig as Config
import logging

discord.utils.setup_logging(level=logging.INFO, root=True)


class CodeReviewBot(Client):
    def __init__(self):
        intents = Intents.default()
        intents.members = True
        intents.message_content = True
        intents.guilds = True

        # initialize DB for the first time
        DB()

        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_guild_join(self, guild: Guild):
        await SyncController.sync_commands(self.tree, guild)


async def main():
    client = CodeReviewBot()
    tree = client.tree
    async with client:
        tree.add_command(CodeReviewCommands(tree, client))
        tree.add_command(SyncCommands(tree, client))
        await client.start(Config.CONFIG["Secrets"]["Discord"]["Token"])


if __name__ == "__main__":
    asyncio.run(main())
