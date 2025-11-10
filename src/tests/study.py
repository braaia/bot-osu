from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))  # adiciona src/ ao sys.path

from server.secrets import *
from server.tokens_utils import *
import urllib.parse, requests, json, irc.client, time

from datetime import timedelta

def segundos_para_string_minutos(segundos):
    # Converte segundos para um objeto timedelta
    tempo = timedelta(seconds=segundos)

    # Formata para uma string 'HH:MM:SS'
    # Para uma string apenas de minutos, use o seguinte:
    minutos = tempo.total_seconds() / 60
    return f"{minutos:.2f} minutos"

segundos = 125
# print(segundos_para_string_minutos(segundos))

base_url = "https://osu.ppy.sh/api/v2"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "response_type": "code",
    "scope": scope
}

data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "code": code,
    "grant_type": "authorization_code",
    "redirect_uri": redirect_uri
}

# auth_url = "https://osu.ppy.sh/oauth/authorize?" + urllib.parse.urlencode(params)
# print(auth_url)

# r = requests.post("https://osu.ppy.sh/oauth/token", data=data)
# print(json.dumps(r.json(), indent=4))

def UserBeatmapScore(beatmap: int, user: int):
    r = requests.get(base_url + f"/beatmaps/{beatmap}/scores/users/{user}", headers=headers)
    data = r.json()

    organized = {
        "beatmap_id": data["score"]["beatmap"]["beatmapset_id"],
        "rank_position": data.get("position"),
        "max_combo": data["score"]["max_combo"],
        "rank": data["score"]["rank"],
        "accuracy": data["score"]["accuracy"],
        "mods": data["score"]["mods"],
        "score": data["score"]["score"],
        "statistics": data["score"]["statistics"]
    }

    print(json.dumps(organized, indent=4))

# UserBeatmapScore(4303461, 20866109)

def GetUserScores(user, type):
    params = {
        "include_fails": 1,
        "limit": 5
    }
    
    r = requests.get(base_url + f"/users/{user}/scores/{type}", params=params, headers=headers)
    data = r.json()

    print(json.dumps(data, indent=4))

# GetUserScores(20866109, "recent")

def CreateNewPM(target_id, message, is_action):
    data = {
        "target_id": target_id,
        "message": message,
        "is_action": is_action
    }

    r = requests.post(base_url + f"/chat/new", json=data, headers=headers)

    print(json.dumps(r.json(), indent=4))

# CreateNewPM(35340610, "oiiiii", False)

def GetBeatmap(beatmap):
    r = requests.get(base_url + f"/beatmaps/{beatmap}", headers=headers)
    data = r.json()

    print(json.dumps(data, indent=4))

# GetBeatmap(4303461)

# Configurações de conexão
server = "irc.ppy.sh"
port = 6667
nickname = "Braia"  # o mesmo nome da sua conta no osu!
password = "3fadb0a7"  # token que você pegou em https://osu.ppy.sh/p/irc


# COMMANDS = {
#     "help": lambda c, s: c.privmsg(s, "Comandos disponíveis: &ping, &say [mensagem para o bot enviar]"),
#     "ping": lambda c, s: c.privmsg(s, "Pong!")
# }

# # Detecta quem enviou msg no PV
# def on_privmsg(connection, event):
#     sender = irc.client.NickMask(event.source).nick
#     message = event.arguments[0].strip()

#     print(f"Mensagem privada de {sender}: {message}")

#     if not message.startswith("&"):
#         return

#     cmd = message[1:].lower()
#     if cmd in COMMANDS:
#         COMMANDS[cmd](connection, sender)
#     # elif message.lower().startswith("&say "):
#     #     textSay = message[5:]
#     #     connection.privmsg(sender, f"Você disse: {textSay}")


# # Envia uma msg para o BanchoBot toda vez q se conectar ao Bancho
# def on_connect(connection, event):
#     print("\nConectado ao Bancho!\n")
#     # exemplo: enviar uma mensagem automática ao conectar
#     connection.privmsg("BanchoBot", "Olá!")

# def main():
#     client = irc.client.Reactor()

#     try:
#         c = client.server().connect(server, port, nickname, password=password)
#     except irc.client.ServerConnectionError as e:
#         print(e)
#         exit(1)

#     c.add_global_handler("welcome", on_connect)
#     c.add_global_handler("privmsg", on_privmsg)

#     client.process_forever()

# if __name__ == "__main__":
#     main()