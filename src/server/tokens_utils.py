import os, json, httpx
from .secrets import client_id, client_secret  # usando import relativo com . para importar do mesmo diretório

token_file = "tokens.json"

access_token = ""
refresh_token = ""

async def load_tokens():
    global access_token, refresh_token
    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            tokens = json.load(f)
            access_token = tokens.get("access_token", "")
            refresh_token = tokens.get("refresh_token", "")

async def save_tokens(tokens):
    with open(token_file, "w") as f:
        json.dump(tokens, f, indent=4)

async def refresh():
    global access_token, refresh_token
    
    await load_tokens()

    if not refresh_token:
        print("❌ Nenhum refresh_token salvo! Faça login com authorization_code primeiro.")
        return

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    head = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as cli:
        r = await cli.post("https://osu.ppy.sh/oauth/token", headers=head, data=data)

    if r.status_code == 200:
        tokens = r.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

        await save_tokens(tokens)
        print("\n✅ Tokens atualizados e salvos!\n")
    else:
        print("\n❌ Falha ao atualizar tokens:\n", r.text)