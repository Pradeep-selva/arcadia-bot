import os
import re
import json
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

ARCADIA_ID = str(os.getenv('ARCADIA_ID'))

dirname = os.path.dirname(__file__)
data_filename = os.path.join(dirname, '../data.json')


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if str(msg.channel.guild.id) == ARCADIA_ID:
            custom_emojis = re.findall(r'<:\w*:\d*>', msg.content)

            if (len(custom_emojis) > 0):
                datas = {}
                custom_emojis = [
                    e.split(':')[1].replace('>', '') for e in custom_emojis
                ]

                emotes = list()
                for i in range(len(custom_emojis)):
                    if (custom_emojis[i] not in emotes
                            and custom_emojis[i][:2] != "GW"):
                        emotes.append(custom_emojis[i])

                if custom_emojis:
                    with open(data_filename) as f:
                        d = json.load(f)
                        p = list()

                        for i in d["emotes"]:
                            if (i["name"] in emotes):
                                p.append(i["name"])
                                count = int(i["count"]) + 1
                                i["count"] = str(count)
                        for i in range(len(emotes)):
                            if (emotes[i] not in p):
                                c = {"name": emotes[i], "count": 1}
                                d["emotes"].append(c)
                        datas = d
                    with open(data_filename, "w") as f:
                        json.dump(datas, f)

        if (not (msg.author.bot) and str(msg.channel.guild.id) == ARCADIA_ID
                and not ("bot" in msg.channel.name)):
            id = msg.author.id
            name = msg.author.name

            datas = {}
            c = 0

            with open(data_filename) as f:
                datas = json.load(f)

                for i in datas["xp"]:

                    if (i["id"] == id):
                        count = int(i["count"]) + 1
                        i["count"] = str(count)
                        c = c + 1

                if (c == 0):
                    c = {"name": name, "count": 1, "id": id}
                    datas["xp"].append(c)

            with open(data_filename, "w") as f:
                json.dump(datas, f)

    @commands.command(name='topmsg',
                      help='displays users with top 10 messages(every 24h)')
    async def topmsg(self, ctx):
        embed = discord.Embed(
            title="Users with top 10 message count for today", color=0x1FEAEA)

        with open(data_filename) as f:
            d = json.load(f)
            a = sorted(d["xp"], key=lambda i: int(i["count"]), reverse=True)
            c = 1
            desc = ""
            for i in a:
                if (c == 11):
                    break
                if c == 1:
                    desc = desc + "\n **{}.**   `{}` : {}".format(
                        c, i["name"], i["count"])
                else:
                    desc = desc + "\n **{}.** `{}` : {}".format(
                        c, i["name"], i["count"])
                c = c + 1
            embed.description = desc
            await ctx.message.channel.send(embed=embed)

    @commands.command(name="msgcount",
                      help='sends message count of a user(reset every 24h)')
    async def msgcount(self, ctx, user=''):
        sid = ctx.message.author.id
        name = ctx.message.author.name
        usrobj = ctx.message.author
        if (user != ''):
            temp = re.findall(r'\d+', user)
            res = list(map(int, temp))
            id = 0
            for i in range(len(res)):
                id = (id * 10) + res[i]
            c = 0
            sid = id

            usrobj = discord.utils.find(lambda m: m.id == id,
                                        ctx.message.channel.guild.members)
            if (not usrobj):
                await ctx.channel.send("The specified user is not found!")
                return

            name = usrobj.name
        d = {}

        embed = discord.Embed(title="Message count for {}".format(name),
                              color=0x00ff00)
        with open(data_filename) as f:
            d = json.load(f)

            for i in d["xp"]:
                if (i["id"] == sid):

                    embed.add_field(name="Name:",
                                    value=i["name"],
                                    inline=False)
                    embed.add_field(name="Messages today:",
                                    value=i["count"],
                                    inline=False)
                    embed.add_field(name="ID:", value=i["id"], inline=False)
                    embed.set_thumbnail(url=usrobj.avatar_url)

                    await ctx.channel.send(embed=embed)
                    return

        await ctx.channel.send("```The user has sent no messages```")

    @commands.command(name='emoteUsage',
                      help='displays emote usage count over the time',
                      aliases=['emoteusage'])
    async def say(self, ctx, name=''):
        a = {}
        if (ctx.message.channel.name == "emote-usage" or name != ''):
            with open(data_filename) as f:
                d = json.load(f)
                if (len(d["emotes"]) == 0):
                    await ctx.message.channel.send(
                        "```No emote usage data has been tracked so far```")
                    return
                if (name == ''):
                    a = sorted(d["emotes"], key=lambda i: int(i["count"]))

                    for i in a:
                        await ctx.message.channel.send("{} : {}".format(
                            i["name"], i["count"]))
                    return
                else:
                    c = 0
                    for i in d["emotes"]:
                        if (name.lower() in i["name"].lower()):
                            embed = discord.Embed(
                                title="Emote usage of {}".format(i["name"]),
                                color=0x00ff00)
                            embed.add_field(name="Count:",
                                            value=i["count"],
                                            inline=False)
                            await ctx.channel.send(embed=embed)
                            return
                    await ctx.channel.send(
                        "```Usage of this emote is not found```")
                    return
        else:
            await ctx.message.channel.send(
                "```This is a staff exclusive command```")


def setup(bot):
    bot.add_cog(Stats(bot))
