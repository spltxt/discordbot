import discord
import requests
import time
from data import *
from discord.ext import commands

#ког, содержащий команду !recent (Чек последних 10 ранов персонажа)
class Recent(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['recent', 'к'])
    async def r(self, ctx, char_name, server_name = None):
        char_name = char_name.capitalize()
        if not server_name:
            server_name = 'howling-fjord'
        elif server_name in realms:
            server_name = realms[server_name]
        params = {
            'region': 'eu', 'realm': server_name, 'name': char_name,
            'fields': 'mythic_plus_recent_runs'
        }

        jsond = requests.get('https://raider.io/api/v1/characters/profile', params=params)

        if jsond.status_code != 200:
            print("Персонаж не найден.")

        # with open('log.txt', 'a', encoding='utf-8') as log:
        #     log.write(f'{time.asctime()} - {ctx.author} произвел чек 10 последних ранов персонажа {char_name} {server_name}\n')
        #     log.close()

        jsondata = jsond.json()
        try:
            i = 'dungeon'
            dungeons = []
            mythic_lvl = []
            clear_time_ms = []
            num_keystone_upgrades = []
            completed_at = []
            timer = []
            for i in jsondata['mythic_plus_recent_runs']:
                dungeons.append(i['short_name'])
                mythic_lvl.append(i['mythic_level'])
                clear_time_ms.append(round(float(i['clear_time_ms'] / 1000 / 60), 1))
                num_keystone_upgrades.append(i['num_keystone_upgrades'])
                completed_at.append((i['completed_at'])[0:10]) # отбрасываю время
                timer.append(round(float(i['par_time_ms'] / 1000 / 60), 0))
            affixes = []
            for j in range(10):
                for i in range(0,4):
                    affixes.append(jsondata['mythic_plus_recent_runs'][j]['affixes'][i]['name'])
            embed = discord.Embed(title=f'{char_name} - 10 последних пройденных ключей', color=discord.Colour.green())
            embed.add_field(name=f'[{completed_at[0]}] - {dungeons[0]} {mythic_lvl[0]} уровня за {clear_time_ms[0]}/{int(timer[0])}:00 минут на +{num_keystone_upgrades[0]}.', value=f'Аффиксы: {affixes[0]}, {affixes[1]}, {affixes[2]}, {affixes[3]}.',inline=False)
            embed.add_field(name=f'[{completed_at[1]}] - {dungeons[1]} {mythic_lvl[1]} уровня за {clear_time_ms[1]}/{int(timer[1])}:00 минут на +{num_keystone_upgrades[1]}.', value=f'Аффиксы: {affixes[4]}, {affixes[5]}, {affixes[6]}, {affixes[7]}.',inline=False)
            embed.add_field(name=f'[{completed_at[2]}] - {dungeons[2]} {mythic_lvl[2]} уровня за {clear_time_ms[2]}/{int(timer[2])}:00 минут на +{num_keystone_upgrades[2]}.', value=f'Аффиксы: {affixes[8]}, {affixes[9]}, {affixes[10]}, {affixes[11]}.',inline=False)
            embed.add_field(name=f'[{completed_at[3]}] - {dungeons[3]} {mythic_lvl[3]} уровня за {clear_time_ms[3]}/{int(timer[3])}:00 минут на +{num_keystone_upgrades[3]}.', value=f'Аффиксы: {affixes[12]}, {affixes[13]}, {affixes[14]}, {affixes[15]}.',inline=False)
            embed.add_field(name=f'[{completed_at[4]}] - {dungeons[4]} {mythic_lvl[4]} уровня за {clear_time_ms[4]}/{int(timer[4])}:00 минут на +{num_keystone_upgrades[4]}.', value=f'Аффиксы: {affixes[16]}, {affixes[17]}, {affixes[18]}, {affixes[19]}.',inline=False)
            embed.add_field(name=f'[{completed_at[5]}] - {dungeons[5]} {mythic_lvl[5]} уровня за {clear_time_ms[5]}/{int(timer[5])}:00 минут на +{num_keystone_upgrades[5]}.', value=f'Аффиксы: {affixes[20]}, {affixes[21]}, {affixes[22]}, {affixes[23]}.',inline=False)
            embed.add_field(name=f'[{completed_at[6]}] - {dungeons[6]} {mythic_lvl[6]} уровня за {clear_time_ms[6]}/{int(timer[6])}:00 минут на +{num_keystone_upgrades[6]}.', value=f'Аффиксы: {affixes[24]}, {affixes[25]}, {affixes[26]}, {affixes[27]}.',inline=False)
            embed.add_field(name=f'[{completed_at[7]}] - {dungeons[7]} {mythic_lvl[7]} уровня за {clear_time_ms[7]}/{int(timer[7])}:00 минут на +{num_keystone_upgrades[7]}.', value=f'Аффиксы: {affixes[28]}, {affixes[29]}, {affixes[30]}, {affixes[31]}.',inline=False)
            embed.add_field(name=f'[{completed_at[8]}] - {dungeons[8]} {mythic_lvl[8]} уровня за {clear_time_ms[8]}/{int(timer[8])}:00 минут на +{num_keystone_upgrades[8]}.', value=f'Аффиксы: {affixes[32]}, {affixes[33]}, {affixes[34]}, {affixes[35]}.',inline=False)
            embed.add_field(name=f'[{completed_at[9]}] - {dungeons[9]} {mythic_lvl[9]} уровня за {clear_time_ms[9]}/{int(timer[9])}:00 минут на +{num_keystone_upgrades[9]}.', value=f'Аффиксы: {affixes[36]}, {affixes[37]}, {affixes[38]}, {affixes[39]}.',inline=False)
            await ctx.send(embed=embed)

        except IndexError:
            embed = discord.Embed(title=f'{char_name} ещё не успел в этом сезоне закрыть 10 ключей.', color=discord.Colour.red())
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Recent(client))
