import discord, os
from server.tokens_utils import refresh
from discord.ext import commands

base_url = "https://osu.ppy.sh/api/v2"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="&", intents=intents)

COGS = "bot"

async def load_cogs():
	for arq in os.listdir(COGS):
		if arq.endswith(".py"):
			await bot.load_extension(f"{COGS}.{arq[:-3]}")

@bot.event
async def on_ready():
	await refresh()
	await load_cogs()

@bot.command()
async def sync(ctx:commands.Context):
	if ctx.author.id == 599240585768861727:
		sincs = await bot.tree.sync()
		print(f"{len(sincs)} comandos sincronizados!")
	else:
		await ctx.reply("Sai fora safado!!! 😝😝")

bot.run("MTQzNjM0OTM0MDM0NzI2OTE1MA.GrozR_.53jXGo314NYnWm-AxYe0CJhf0q0nHczjSmOgYo") 