from discord.ext import commands
import aiohttp
import discord
import os
import traceback
import re
import dotenv
import logging


async def get_prefix(bot, message):
  extras = ["manager*", "jm*", "e*"]

  comp = re.compile(
      "^(" + "|".join(map(re.escape, extras)) + ").*", flags=re.I)
  match = comp.match(message.content)
  if match is not None:
    extras.append(match.group(1))

  if await bot.is_owner(message.author):
    extras.append("")


  return commands.when_mentioned_or(*extras)(bot, message)

class ManagerBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def start(self,*args, **kwargs):
        self.session = aiohttp.ClientSession()
        await super().start(*args, **kwargs)

    async def close(self):
        await self.session.close()
        await super().close()


bot = ManagerBot(command_prefix=(get_prefix), intents=discord.Intents.all(), chunk_guilds_at_startup=False,
                 strip_after_prefix=True, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))


for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    try:
      bot.load_extension(f'cogs.{filename[:-3]}')
    except commands.errors.ExtensionError:
      traceback.print_exc()

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)

handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')

bot.change_presence(status=discord.Status.online, activity=discord.Activity(
    type=discord.ActivityType.listening, name=f"Testing by JDJG about vpses"))

bot.run(os.environ["TOKEN"])
