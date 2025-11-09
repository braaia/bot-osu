import discord
from discord import app_commands
from discord.ext import commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.helpText = "Para usar o comando \"recommend\", você precisa adicionar o ID da dificuldade (diff_id) escolhida do beatmap que vc quer, que é o ultimo ID que aparece na URL do browser, por exemplo: \nosu.ppy.sh/beatmapsets/2058976#osu/**4303461**\n\nO ID \"4303461\" é a ultima dificuldade do mapa Heat Abnormal e é esse ID que deve ser utilizado para recomendação de mapas."
        super().__init__()

    @commands.command(name="Help")
    async def ajuda(self, ctx:commands.Context):
        await ctx.reply(self.helpText)

    @app_commands.command(description="Use caso precise de ajuda nos comandos")
    async def help_app(self, interact:discord.Interaction):
        await interact.response.send_message(self.helpText, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCommands(bot))