import discord, httpx, json
from server.tokens_utils import load_tokens, access_token
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from discord import app_commands
from discord.ext import commands
from server.database import *

class MapsCrud(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://osu.ppy.sh/api/v2"
        self._Session = sessionmaker(engine)
        super().__init__()

    async def get_headers(self):
        await load_tokens()
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @app_commands.command(description="Recomende mapas para ser adicionado ao bot!!")
    async def recommend_maps(self, interact:discord.Interaction, diff_id: int):
        # Adia a resposta para evitar timeout de 3 segundos
        # Depois que você usa defer, precisa usar followup para enviar mensagens
        # Defer() faz o bot mostrar "está pensando..." e dá mais tempo
        await interact.response.defer()

        async with httpx.AsyncClient() as cli:
            r = await cli.get(self.base_url + f"/beatmaps/{diff_id}", headers=await self.get_headers(), timeout=10.0)

            if r.status_code == 200:
                data = r.json()
                organized = {
                    "beatmap_id": data["beatmapset_id"],
                    "artist": data["beatmapset"]["artist"],
                    "title": data["beatmapset"]["title"],
                    "star_rating": data["difficulty_rating"],
                    "ar": data["ar"],
                    "bpm": data["bpm"],
                    "length": data["total_length"],
                    "ranked": data["ranked"],
                    "url": data["url"]
                }

                with self._Session() as session:
                    exists_in_rcm_maps = session.query(RecommendedMaps).filter(RecommendedMaps.diff_id == diff_id).first()
                    exists_in_ar0 = session.query(ARZero).filter(ARZero.diff_id == diff_id).first()
                    exists_in_ar8 = session.query(AROito).filter(AROito.diff_id == diff_id).first()
                    exists_in_ar10 = session.query(ARDez).filter(ARDez.diff_id == diff_id).first()

                    if exists_in_rcm_maps or exists_in_ar0 or exists_in_ar8 or exists_in_ar10:
                        await interact.followup.send("❌ Este mapa já foi adicionado anteriormente!")
                        return

                    maap = RecommendedMaps(
                        beatmap_id=organized["beatmap_id"],
                        diff_id=diff_id,
                        artist=organized["artist"],
                        title=organized["title"],
                        star_rating=organized["star_rating"],
                        ar=organized["ar"],
                        bpm=organized["bpm"],
                        length=organized["length"],
                        ranked=organized["ranked"],
                        url=organized["url"]
                    )
                    session.add(maap)
                    session.commit()
                    
                await interact.followup.send(f"✅ Mapa \"{organized['artist']} - {organized['title']}\" recomendado com sucesso!")
                await interact.followup.send(json.dumps(organized, indent=4))
            else:
                await interact.followup.send("❌ Você digitou o ID do mapa incorretamente!")

    @app_commands.command(description="Adicionar mapas ao bot.")
    async def add_maps(self, interact:discord.Interaction, diff_id: int):
        if interact.user.id == 599240585768861727:
            await interact.response.defer()
            
            async with httpx.AsyncClient() as cli:
                r = await cli.get(self.base_url + f"/beatmaps/{diff_id}", headers=await self.get_headers(), timeout=10.0)

                if r.status_code == 200:
                    data = r.json()
                    organized = {
                        "beatmap_id": data["beatmapset_id"],
                        "artist": data["beatmapset"]["artist"],
                        "title": data["beatmapset"]["title"],
                        "star_rating": data["difficulty_rating"],
                        "ar": data["ar"],
                        "bpm": data["bpm"],
                        "length": data["total_length"],
                        "ranked": data["ranked"],
                        "url": data["url"]
                    }

                    with self._Session() as session:
                        # Verifica se o diff_id já existe em alguma tabela
                        exists_in_rcm_maps = session.query(RecommendedMaps).filter(RecommendedMaps.diff_id == diff_id).first()
                        exists_in_ar0 = session.query(ARZero).filter(ARZero.diff_id == diff_id).first()
                        exists_in_ar8 = session.query(AROito).filter(AROito.diff_id == diff_id).first()
                        exists_in_ar10 = session.query(ARDez).filter(ARDez.diff_id == diff_id).first()

                        if exists_in_rcm_maps:
                            session.delete(exists_in_rcm_maps)
                            session.commit()

                        if exists_in_ar0 or exists_in_ar8 or exists_in_ar10:
                            await interact.followup.send("❌ Este mapa já foi adicionado anteriormente!")
                            return

                        # O zero desse código garante que ar_value sempre exista
                        ar_value = organized.get("ar", 0)
                        if ar_value == 0:
                            map = ARZero(
                                beatmap_id=organized["beatmap_id"],
                                diff_id=diff_id,
                                artist=organized["artist"],
                                title=organized["title"],
                                star_rating=organized["star_rating"],
                                ar=organized["ar"],
                                bpm=organized["bpm"],
                                length=organized["length"],
                                ranked=organized["ranked"],
                                url=organized["url"]
                            )
                            map_list = AllMaps(
                                beatmap_id=organized["beatmap_id"],
                                diff_id=diff_id,
                                artist=organized["artist"],
                                title=organized["title"],
                                star_rating=organized["star_rating"],
                                ar=organized["ar"],
                                bpm=organized["bpm"],
                                length=organized["length"],
                                ranked=organized["ranked"],
                                url=organized["url"]
                            )
                            session.add(map_list)
                            session.add(map)
                            session.commit()
                        elif ar_value <= 8:
                            map = AROito(
                                beatmap_id=organized["beatmap_id"],
                                diff_id=diff_id,
                                artist=organized["artist"],
                                title=organized["title"],
                                star_rating=organized["star_rating"],
                                ar=organized["ar"],
                                bpm=organized["bpm"],
                                length=organized["length"],
                                ranked=organized["ranked"],
                                url=organized["url"]
                            )
                            map_list = AllMaps(
                                beatmap_id=organized["beatmap_id"],
                                diff_id=diff_id,
                                artist=organized["artist"],
                                title=organized["title"],
                                star_rating=organized["star_rating"],
                                ar=organized["ar"],
                                bpm=organized["bpm"],
                                length=organized["length"],
                                ranked=organized["ranked"],
                                url=organized["url"]
                            )
                            session.add(map_list)
                            session.add(map)
                            session.commit()
                        elif ar_value <= 10:
                            map = ARDez(
                                beatmap_id=organized["beatmap_id"],
                                diff_id=diff_id,
                                artist=organized["artist"],
                                title=organized["title"],
                                star_rating=organized["star_rating"],
                                ar=organized["ar"],
                                bpm=organized["bpm"],
                                length=organized["length"],
                                ranked=organized["ranked"],
                                url=organized["url"]
                            )
                            map_list = AllMaps(
                                beatmap_id=organized["beatmap_id"],
                                diff_id=diff_id,
                                artist=organized["artist"],
                                title=organized["title"],
                                star_rating=organized["star_rating"],
                                ar=organized["ar"],
                                bpm=organized["bpm"],
                                length=organized["length"],
                                ranked=organized["ranked"],
                                url=organized["url"]
                            )
                            session.add(map_list)
                            session.add(map)
                            session.commit()
                        else:
                            map = ARDez(
                                beatmap_id=organized["beatmap_id"],
                                diff_id=diff_id,
                                artist=organized["artist"],
                                title=organized["title"],
                                star_rating=organized["star_rating"],
                                ar=organized["ar"],
                                bpm=organized["bpm"],
                                length=organized["length"],
                                ranked=organized["ranked"],
                                url=organized["url"]
                            )
                            map_list = AllMaps(
                                beatmap_id=organized["beatmap_id"],
                                diff_id=diff_id,
                                artist=organized["artist"],
                                title=organized["title"],
                                star_rating=organized["star_rating"],
                                ar=organized["ar"],
                                bpm=organized["bpm"],
                                length=organized["length"],
                                ranked=organized["ranked"],
                                url=organized["url"]
                            )
                            session.add(map_list)
                            session.add(map)
                            session.commit()
                            
                    await interact.followup.send(f"✅ Mapa \"{organized['artist']} - {organized['title']}\" adicionado com sucesso!")
                    await interact.followup.send(json.dumps(organized, indent=4))
                else:
                    await interact.followup.send("❌ Você digitou o ID do mapa incorretamente!")
        else:
            await interact.response.send_message("Sai fora safado!!! 😝😝")

    @app_commands.command(description="Faça uma listagem de todos os mapas contidos no bot!")
    @app_commands.choices(
        sort_by=[
            app_commands.Choice(name="Star Rating", value="star_rating"),
            app_commands.Choice(name="AR", value="ar"),
            app_commands.Choice(name="BPM", value="bpm"),
            app_commands.Choice(name="Length", value="length"),
        ],
        decrescent=[
            app_commands.Choice(name="Descending order", value=1),
            app_commands.Choice(name="Ascending order", value=0)
        ],
        status=[
            app_commands.Choice(name="Loved", value=4),
            app_commands.Choice(name="Qualified", value=3),
            app_commands.Choice(name="Approved", value=2),
            app_commands.Choice(name="Ranked", value=1),
            app_commands.Choice(name="Pending", value=0),
            app_commands.Choice(name="Graveyard", value=-2)
        ])
    async def display_recommended_maps(self, interact:discord.Interaction, sort_by: str = None, decrescent: int = 0, status: int = None):
        await interact.response.defer()

        with self._Session() as session:
            query = session.query(AllMaps)
            
            # Aplicar ordenação se especificada
            if sort_by is not None and decrescent == 0:
                sort_attr = getattr(AllMaps, sort_by)
                query = query.order_by(sort_attr)
            elif sort_by is not None and decrescent == 1:		
                sort_attr = getattr(AllMaps, sort_by)
                query = query.order_by(desc(sort_attr))
            
            # Filtrar por status se especificado
            if status is not None:
                query = query.filter(AllMaps.ranked == status)
            
            maps = query.all()
            
            if not maps:
                await interact.followup.send("Nenhum mapa encontrado!")
                return
                
            # Criar mensagem com os mapas
            message = "**Lista de Mapas:**\n\n"
            for map in maps:
                message += f"**[{map.artist} - {map.title}]({map.url})**\n"
                message += f"★ {map.star_rating:.2f} | AR {map.ar} | BPM {map.bpm} | {map.length}s\n\n"
                
                # Se a mensagem ficar muito grande, envia em partes
                if len(message) > 1500:  # Discord tem limite de 2000 caracteres
                    await interact.followup.send(message)
                    message = "**Continuação:**\n\n"
            
            # Envia o restante da mensagem se houver
            if message:
                await interact.followup.send(message)

    @app_commands.command(description="Deletar mapas recomendados.")
    @app_commands.choices(ar_choice=[
        app_commands.Choice(name="<=AR10", value="ARDez"),
        app_commands.Choice(name="<=AR8", value="AROito"),
        app_commands.Choice(name="AR0", value="ARZero")
    ])
    async def delete_maps(self, interact: discord.Interaction, diff_id: int, ar_choice: str):
        # Só para servidores
        if interact.guild is None:
            await interact.response.send_message("Este comando só pode ser usado dentro de um servidor.", ephemeral=True)
            return

        # interact.user é um Member no contexto de guilda
        if not interact.user.guild_permissions.administrator:
            await interact.response.send_message("Sai fora safado!!! 😝😝", ephemeral=True)
            return

        # Mapear o valor da escolha para a classe do modelo
        choice_map = {
            "ARDez": ARDez,
            "AROito": AROito,
            "ARZero": ARZero,
        }

        model_chs = choice_map.get(ar_choice)
        if model_chs is None:
            await interact.response.send_message("Escolha inválida.", ephemeral=True)
            return

        with self._Session() as session:
            music = session.query(model_chs).first()

            map = session.query(model_chs).filter(model_chs.diff_id == diff_id).first()
            if not map:
                await interact.response.send_message("Mapa não encontrado nessa tabela.", ephemeral=True)
                return
            
            session.delete(map)
            session.commit()

        await interact.response.send_message(f"✅ Mapa \"{music.artist} - {music.title}\" deletado com sucesso.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(MapsCrud(bot))