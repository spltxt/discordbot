import discord
from discord.ext import commands

#ког для событий и команды !cmd (помощь)
class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("C:\\Users\\user\\Desktop\\discordbot\\members_joined.txt", 'a', encoding='utf-8') as log:
            log.write(f'{time.asctime()} - {member} присоединился к серверу\n')
            log.close()
        print(f'{member} присоеденился к серверу.')

    @commands.Cog.listener()
    async def on_member_remove(self, ctx, member):
        channel = client.get_channel(913354324317458462)
        await channel.message.send(f'{member} покинул сервер')

    @commands.command()
    async def ms(self, ctx):
        await ctx.send(f'Пинг: {round(client.latency * 1000)}ms')

    @commands.command(aliases=['commands'])
    async def cmd(self, ctx):
        await ctx.send('''
Команды:\n\n!rio - [Имя персонажа] [Cервер] - Чек спека, ковенанта, ilvl, тринкетов.
\n!c или !check - [Имя персонажа] [Cервер] - Чек лучшего рана на этой неделе.
\n!r или !recent - [Имя персонажа] [Сервер] - Чек последних 10 ранов персонажа.\n
Сокращения серверов:
сд - Свежеватель, гд - Гордунни, бт - Борейская Тундра, ял - Ясеневый Лес
tm - Tarren Mill, sg - Sanguino, kz - Kazzak, tn - Twisting Nether, hj - Hyjal,
br - Blackrock, dr - Draenor, bl - Burning Legion, ss - Stormscale
''')

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title='Команды:', color= discord.Colour.green())
        embed.add_field(name='!rio', value='[Имя персонажа] [Cервер] - Чек спека, ковенанта, ilvl, тринкетов.', inline=True)
        embed.add_field(name='!c или !check', value='[Имя персонажа] [Cервер] - Чек лучшего рана на этой неделе.', inline=True)
        embed.add_field(name='!r или !recent', value=' [Имя персонажа] [Сервер] - Чек последних 10 ранов персонажа.', inline=True)
        embed.add_field(name='Сокращения серверов:', value='''сд - Свежеватель, гд - Гордунни, бт - Борейская Тундра, ял - Ясеневый Лес
tm - Tarren Mill, sg - Sanguino, kz - Kazzak, tn - Twisting Nether, hj - Hyjal,
br - Blackrock, dr - Draenor, bl - Burning Legion, ss - Stormscale.''')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Utils(client))
