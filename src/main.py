import discord, httpx, json, irc.client, os
from server.database import *
from server.tokens_utils import refresh
from discord.ext import commands

base_url = "https://osu.ppy.sh/api/v2"

# Configurações de conexão
server = "irc.ppy.sh"
port = 6667
nickname = "Braia"
password = "3fadb0a7"  # token que você pegou em https://osu.ppy.sh/p/irc


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


COMMANDS = {
    "help": lambda c, s: c.privmsg(s, "Comandos disponíveis: &ping"),
    "ping": lambda c, s: c.privmsg(s, "Pong!")
}

# Detecta quem enviou msg no PV
def on_privmsg(connection, event):
    sender = irc.client.NickMask(event.source).nick
    message = event.arguments[0].strip()

    print(f"Mensagem privada de {sender}: {message}")

    if not message.startswith("&"):
        return

    cmd = message[1:].lower()
    if cmd in COMMANDS:
        COMMANDS[cmd](connection, sender)
    # elif message.lower().startswith("&say "):
    #     textSay = message[5:]
    #     connection.privmsg(sender, f"Você disse: {textSay}")


# Envia uma msg para o BanchoBot toda vez q se conectar ao Bancho
def on_connect(connection, event):
    print("\nConectado ao Bancho!\n")
    # exemplo: enviar uma mensagem automática ao conectar
    connection.privmsg("BanchoBot", "Olá!")

def main():
    client = irc.client.Reactor()

    try:
        c = client.server().connect(server, port, nickname, password=password)
    except irc.client.ServerConnectionError as e:
        print(e)
        exit(1)

    c.add_global_handler("welcome", on_connect)
    c.add_global_handler("privmsg", on_privmsg)

    client.process_forever()

if __name__ == "__main__":
    main()



bot.run("MTQzNjM0OTM0MDM0NzI2OTE1MA.GrozR_.53jXGo314NYnWm-AxYe0CJhf0q0nHczjSmOgYo")