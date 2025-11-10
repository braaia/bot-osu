from sqlalchemy.orm import sessionmaker
from server.database import User, engine
from server.secrets import server, port, nickname, password
import irc.client

_Session = sessionmaker(engine)


async def save_user(sender, message):
	with _Session() as session:
		user = session.query(User).filter_by(username=sender).first()
		if not user:
			user = User(username=sender, last_message=message)
			session.add(user)
			print(f"[DB] Novo usuário adicionado: {sender}")
		else:
			user.last_message = message  # Atualiza última mensagem
		session.commit()

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