import os
import time
import requests
import json
from googletrans import Translator
import discord
from dotenv import load_dotenv
from discord.ext import commands
import matplotlib.pyplot as plt
from firebase_admin import firestore

db = firestore.client()

load_dotenv()

GOOGLE_API_KEY = str(os.getenv('GOOGLE_API_KEY'))
SEARCH_ENGINE_ID = str(os.getenv('SEARCH_ENGINE_ID'))
BING_API_KEY = str(os.getenv('BING_API_KEY'))


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='ping')
    async def ping(self, ctx):
        await ctx.channel.send('Pong! {0} ms'.format(round(
            self.bot.latency, 1)))

    @commands.command(name="help")
    async def help(self, ctx):
        help = ""
        help += "**__Moderation__**\n"
        help += "`devreset`, `softban`, `emoteDataClear`\n `spamlist`, `spamremove`, `displayspam`\n"
        help += "\n**__Utilities__**\n"
        help += "`aniInfo`, `cf`, `invite`, `ping` \n  `img`, `customhelp`, `custom`, `customdelete`\n`customupdate`, `customlist`, `translate`, `imgStats` \n"
        help += "\n**__Stats__**\n"
        help += "`msgcount`,`emoteUsage`, `topmsg`\n"
        help += "\n**__Fun__**\n"
        help += "`gamerpoints`, `munnirage`, `owo`\n `mock`, `say`, `senpai`\n"
        help += "\n**__Games__**\n"
        help += "`rps`, `rpsscore`, `toprps`"

        embed = discord.Embed(title="List of commands", color=0x1FEAEA)
        embed.description = help

        await ctx.send(embed=embed)

    @commands.command(name='invite', help="creates an invite to server")
    async def send_dm(self, ctx):
        c = await ctx.message.author.create_dm()
        await c.send("https://discord.gg/QjDk45T")
        await ctx.message.channel.send("**Check your DM** 👍")

    @commands.command(name="img", help="displays a relevant image")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def img(self, ctx, *msg):
        query = ' '.join(msg)
        img = ""
        if query == "":
            await ctx.send("What image do u want tho?")
            return

        if query.lower() == "arcadia":
            img = "https://images-ext-1.discordapp.net/external/sc3p-qOYB1jWwkFDfd4i6W7_r-lQP7o9rShmSlNT3zM/%3Fsize%3D256/https/cdn.discordapp.com/avatars/650969739107237900/8aa95ac0cf6413decdfd6c76e9c30f6e.png"
        else:
            key = GOOGLE_API_KEY
            cx = SEARCH_ENGINE_ID

            search_url = f"https://www.googleapis.com/customsearch/v1?key={key}&q={query}&cx={cx}&searchType=image&num=2"

            response = requests.get(search_url)
            data = response.json()

            print(data)

        try:
            if query.lower() == "arcadia":
                pass
            else:
                if data["items"][0]["link"].startswith(
                        "https://lookaside"
                ) or "svg" in data["items"][0]["link"]:
                    img = data["items"][1]["link"]
                else:
                    img = data["items"][0]["link"]
        except KeyError:
            try:
                if data["error"]["code"] == 429:
                    url = "https://bing-image-search1.p.rapidapi.com/images/search"
                    querystring = {"count": "1", "q": query}
                    headers = {
                        'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
                        'x-rapidapi-key': BING_API_KEY
                    }

                    response = requests.request("GET",
                                                url,
                                                headers=headers,
                                                params=querystring)

                    res = json.loads(response.text)
                    print(res)
                    try:
                        img = res["value"][0]["contentUrl"]
                    except KeyError:
                        await ctx.send(f"**No images found for {query}**")
                    else:
                        embed = discord.Embed(
                            title=f"Image result for {query}", color=0x1FEAEA)
                        embed.set_image(url=img)

                        await ctx.send(embed=embed)
            except KeyError:
                await ctx.send(f"**No images found for {query}**")
                return
            else:
                print(img)
        else:
            print(img)
            embed = discord.Embed(title=f"Image result for {query}",
                                  color=0x1FEAEA)
            embed.set_image(url=img)

            await ctx.send(embed=embed)
        
        doc_ref = db.collection(u'img-stats').document(str(ctx.message.author.name))

        if not(doc_ref.get().exists):
            doc_ref.set({u'uses':1})
        else:
            doc_ref.update({u'uses': firestore.Increment(1)})

@commands.command(name="imgStats", help="get stats on +img")
async def imgStats(ctx, *msg):
    label = list()
    sizes = list()

    doc_ref = db.collection(u'img-stats').order_by(u'uses', direction=firestore.Query.DESCENDING)
    docs = list(doc_ref.stream())[:20]

    for doc in docs:
        label.append(doc.id)
        sizes.append(doc.to_dict()["uses"])
    
    explode = [0]*len(label)
    explode[sizes.index(max(sizes))] = 0.1

    print("+imgStats", label,sizes,explode)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=label, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal') 

    plt.savefig("chart.png")

    await ctx.channel.send(file=discord.File('chart.png'), content="**Top 20 +img users**")


    @commands.command(name="cf", help="View your codeforces profile summary")
    async def cf(self, ctx, *msg):
        msg = ' '.join(msg)
        if (msg):
            userInfo = "https://codeforces.com/api/user.info?handles="

            data = requests.get(userInfo + msg)
            data = data.json()

            if data["status"] == "OK":
                result = data["result"][0]
                embed = discord.Embed(title="Codeforces Summary of {}".format(
                    result["handle"]),
                                      color=0x00ff00)

                try:
                    isRanked = result["rank"] != None
                except KeyError:
                    isRanked = False

                if isRanked:
                    embed.add_field(name="Current Rank: ",
                                    value=result["rank"],
                                    inline=False)
                    embed.add_field(name="Current Rating: ",
                                    value=result["rating"],
                                    inline=False)
                    embed.add_field(name="Max Rating: ",
                                    value=result["maxRating"],
                                    inline=False)
                    embed.add_field(name="Max Rank: ",
                                    value=result["maxRank"],
                                    inline=False)
                else:
                    embed.add_field(name="The user is currently:",
                                    value="Unrated",
                                    inline=False)
                embed.add_field(name="Contributions: ",
                                value=result["contribution"],
                                inline=False)
                timeHuman = time.strftime(
                    '%Y-%m-%D %H:%M:%S',
                    time.localtime(result["lastOnlineTimeSeconds"]))
                embed.add_field(name="Last Online: ",
                                value=timeHuman,
                                inline=False)

                thumbUrl = "https://{}".format(result["titlePhoto"][2:])
                embed.set_thumbnail(url=thumbUrl)

                await ctx.message.channel.send(embed=embed)
            else:
                await ctx.message.channel.send("***USER NOT FOUND***")
        else:
            await ctx.channel.send(
                "**Please enter a user to view their cf summary**")

    @commands.command(name="aniInfo", help="get an anime's info")
    async def anime(self, ctx, *msg):
        query = ("%20".join(msg)).strip()
        searchurl = "https://kitsu.io/api/edge/anime?filter[TEXT]="

        data = requests.get(searchurl + query)
        data = data.json()

        result = data["data"][0]

        try:
            isFound = result["id"] is not None
        except KeyError:
            isFound = False

        if isFound:
            anime = result["attributes"]
            embed = discord.Embed(title="{}".format(anime["canonicalTitle"]),
                                  color=0x00ff00)
            if (len(anime["synopsis"]) <= 1024):
                embed.add_field(name="Synopsis: ",
                                value=anime["synopsis"],
                                inline=False)
            embed.add_field(name="Rating: ",
                            value=anime["averageRating"],
                            inline=False)
            embed.add_field(name="Popularity Rank: ",
                            value=anime["popularityRank"],
                            inline=False)
            embed.add_field(name="Status: ",
                            value=anime["status"],
                            inline=False)
            embed.add_field(name="Episodes: ",
                            value=anime["episodeCount"],
                            inline=False)

            thumbUrl = anime["posterImage"]["small"]
            embed.set_thumbnail(url=thumbUrl)

            await ctx.message.channel.send(embed=embed)

            if (len(anime["synopsis"]) > 1024):
                await ctx.message.channel.send(
                    "**SYNOPSIS** \n ```{}```".format(anime["synopsis"]))
        else:
            await ctx.message.channel.send("```Anime not found!```")

    @commands.command(name='translate',
                      help='translate foreign text to english')
    async def trans(self, ctx, *msg):
        strmsg = " ".join(msg)

        translator = Translator()
        translation = translator.translate(strmsg)

        await ctx.channel.send("`{}`".format(translation.text))


def setup(bot):
    bot.add_cog(Utilities(bot))