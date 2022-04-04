import discord
import time
import requests
from data import *
from discord.ext import commands

class Check(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['check', 'с'])
    async def c(self, ctx, char_name, server_name = None):
        char_name = char_name.capitalize()
        if not server_name:
            server_name = 'howling-fjord'
        elif server_name in realms:
            server_name = realms[server_name]

        params = {
            'region': 'eu', 'realm': server_name, 'name': char_name,
            'fields': 'mythic_plus_weekly_highest_level_runs'
        }

        jsond = requests.get('https://raider.io/api/v1/characters/profile', params=params)

        if jsond.status_code != 200:
            await ctx.send("Персонаж не найден.")

        # with open(logs\\log.txt', 'a', encoding='utf-8') as log:
        #     log.write(f'{time.asctime()} - {ctx.author} произвел чек персонажа {char_name} {server_name}\n')
        #     log.close()

        jsondata = jsond.json()

        # emoji = self.client.get_emoji(906564210622885909)
        best_key = []
        data_needed = ['short_name', 'mythic_level', 'clear_time_ms', 'par_time_ms', 'num_keystone_upgrades']
        if jsondata['mythic_plus_weekly_highest_level_runs'] == []:
            embed = discord.Embed(title=f'Лучший ран {char_name} на этой неделе', color= discord.Colour.red())
            embed.add_field(name=f'На этой неделе {char_name} не закрыл ни одного ключа.', value=f'\u200b', inline=True)
            await ctx.send(embed=embed)
        else:
            affixes = []
            for i in range(0,4):
                affixes.append(jsondata['mythic_plus_weekly_highest_level_runs'][0]['affixes'][i]['name'])
            completed_at = jsondata['mythic_plus_weekly_highest_level_runs'][0]['completed_at']
            completed_at = completed_at[0:10]
            for i in jsondata['mythic_plus_weekly_highest_level_runs'][0]:
                if i in data_needed:
                    best_key.append(jsondata['mythic_plus_weekly_highest_level_runs'][0][i])
            embed = discord.Embed(title=f'Лучший ран {char_name} на этой неделе', color= discord.Colour.green())
            embed.add_field(name=f'{completed_at} {char_name} закрыл {best_key[0]} {best_key[1]} уровня за {round(float(best_key[2]) / 1000 / 60, 2)}/{int((best_key[3]) / 1000 / 60)}:00 минут на +{best_key[4]}', value=f'Аффиксы: {affixes[0]}, {affixes[1]}, {affixes[2]}, {affixes[3]}')
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Check(client))
