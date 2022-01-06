import discord
import requests
import aiohttp
import time
import io
import asyncio
from data import *
from discord.ext import commands

class Rio(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rio(self, ctx, char_name, server_name = None):
        char_name = char_name.capitalize()
        if not server_name:
            server_name = 'howling-fjord'
        elif server_name in realms:
            server_name = realms[server_name]

        params = {
            'region': 'eu', 'realm': server_name, 'name': char_name,
            'fields': 'covenant,gear,raid_progression,guild,mythic_plus_scores_by_season:current'
        }

        jsond = requests.get('https://raider.io/api/v1/characters/profile', params=params)

        if jsond.status_code != 200:
            embed = discord.Embed(title=f'Персонаж {char_name} не найден.', color=discord.Colour.red())
            await ctx.send(embed=embed)


        # with open('logs\\log.txt', 'a', encoding='utf-8') as log:
        #     log.write(f'{time.asctime()} - {ctx.author} произвел поиск персонажа {char_name} {server_name}\n')
        #     log.close()

        jsondata = jsond.json()

        try:
            pic = jsondata['thumbnail_url']
        except KeyError:
            return
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(pic) as resp:
        #         if resp.status != 200:
        #             return
        #         data = io.BytesIO(await resp.read())
        #         await ctx.send(file=discord.File(data, 'char_thumbnail.png'))

        progress = jsondata['raid_progression']['sanctum-of-domination']['mythic_bosses_killed']
        realm = jsondata['realm']
        if realm in realmsru:
            realm = realmsru[realm]
        cclass = classes[jsondata['class']]
        mscore = int(jsondata['mythic_plus_scores_by_season'][0]['scores']['all'])
        gear = jsondata['gear']['item_level_equipped']
        gender = jsondata['gender']
        if gender == 'female':
            race = female[jsondata['race']]
        else:
            race = male[jsondata['race']]
        trink1_name = jsondata['gear']['items']['trinket1']['name']
        if trink1_name in trinkets:
            trink1_name = trinkets[trink1_name]
        trink2_name = jsondata['gear']['items']['trinket2']['name']
        if trink2_name in trinkets:
            trink2_name = trinkets[trink2_name]
        trink1_ilvl = jsondata['gear']['items']['trinket1']['item_level']
        trink2_ilvl = jsondata['gear']['items']['trinket2']['item_level']
        covenant_name = jsondata['covenant']['name']
        renown = jsondata['covenant']['renown_level']
        if covenant_name in covenants:
            covenant_name = covenants[covenant_name]
        spec = specs[jsondata['active_spec_name']]
        if jsondata['guild'] == None:
            embed = discord.Embed(title=f'{char_name} - {realm} - [{mscore}]\n\n{race} - {cclass} специализации {spec}\n', color= discord.Colour.random())
            embed.add_field(name=f'<Нет гильдии>\nSoD - {progress}/10M' , value=f'\u200b', inline=True)
            embed.add_field(name=f'Ковенант - {covenant_name}', value=f'Уровень известности - {renown}', inline=True)
            embed.add_field(name=f'Уровень предметов', value=f'{gear}')
            embed.add_field(name=f'Тринкеты', value=f'{trink1_name} {trink1_ilvl}\n{trink2_name} {trink2_ilvl}', inline=True)
            embed.set_thumbnail(url = pic)
            # embed.set_footer(icon_url=ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
            await ctx.send(embed=embed)

        else:
            guild = jsondata['guild']['name']
            embed = discord.Embed(title=f'{char_name} - {realm} - [{mscore}]\n\n{race} - {cclass} специализации {spec}\n', color= discord.Colour.random())
            embed.add_field(name=f'<{guild}>\nSoD - {progress}/10M' , value='\u200b', inline=True)
            embed.add_field(name=f'Ковенант - {covenant_name}', value=f'Уровень известности - {renown}', inline=True)
            embed.add_field(name=f'Уровень предметов', value=f'{gear}')
            embed.add_field(name=f'Тринкеты', value=f'{trink1_name} {trink1_ilvl}\n{trink2_name} {trink2_ilvl}', inline=True)
            embed.set_thumbnail(url = pic)
            # embed.set_footer(icon_url=ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Rio(client))
