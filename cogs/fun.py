import os
import re
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw

load_dotenv()

GOLD_ID = str(os.getenv('GOLD_ID'))
PRAX_ID = str(os.getenv('PRAX_ID'))


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if (("brick" in message.content.lower())
                or ("bricks" in message.content.lower())
                or (":bricks:" in message.content.lower())):

            await message.add_reaction('🧱')

    @commands.command(
        name='say',
        help=
        'says what you want it to say[type -hide in the end to hide your message]'
    )
    async def say(self, ctx, *msg):

        p = "p"
        print(msg)
        strmsg = ' '.join(msg)
        print(strmsg)
        if (strmsg.endswith("-hide")):
            p = "s"
        if ((msg == "")):
            await ctx.channel.send('I dont know what to say')
        else:
            if (p == "s"):
                await ctx.message.delete()
                await ctx.channel.send(strmsg[:(len(strmsg) - 5)])
            else:
                await ctx.channel.send(strmsg[:(len(strmsg))])

    @commands.command(name='mock',
                      help='Makes things sound more goofy than usual')
    async def mock(self, ctx, *msg):
        p = "p"

        msg = ' '.join(msg).lower()
        strmsg = list()
        for i in range(len(msg)):
            strmsg.append(msg[i])
        for i in range(len(strmsg)):
            if (strmsg[i] == 'c'):
                strmsg[i] = 'K'
            elif (strmsg[i] == 'o'):
                strmsg[i] = '0'
            elif (i % 2 == 0):
                strmsg[i] = strmsg[i].upper()

        strmsg = ''.join(strmsg)

        await ctx.message.channel.send(strmsg)
        await ctx.channel.send(file=discord.File('rishon.png'))

    @commands.command(name='munnirage',
                      help="Add a caption and generate a triggered munni meme")
    async def meme(self, ctx, *msg):
        if "dankus" in ctx.message.channel.name:
            x, y = 3, 3
            text = ""

            msg = ' '.join(msg)

            fname1 = "gold.jpg"
            im = Image.open(fname1)
            pointsize = 15
            fillcolor = "white"
            shadowcolor = "black"

            txt = msg

            font = "arialbd.ttf"
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype(font, pointsize)

            for i in range(len(txt)):

                text = text + txt[i]

                if (i % 20 == 0 and i != 0):
                    if (txt[i + 1] == ' ' or txt[i] == ' '):
                        draw.text((x - 1, y),
                                  text,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x + 1, y),
                                  text,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x, y - 1),
                                  text,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x, y + 1),
                                  text,
                                  font=font,
                                  fill=shadowcolor)

                        draw.text((x - 1, y - 1),
                                  text,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x + 1, y - 1),
                                  text,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x - 1, y + 1),
                                  text,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x + 1, y + 1),
                                  text,
                                  font=font,
                                  fill=shadowcolor)

                        draw.text((x, y), text, font=font, fill=fillcolor)
                        text = ""

                        y = y + 15
                    else:
                        xx = text.rfind(' ')
                        texto = text[:xx].strip()

                        draw.text((x - 1, y),
                                  texto,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x + 1, y),
                                  texto,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x, y - 1),
                                  texto,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x, y + 1),
                                  texto,
                                  font=font,
                                  fill=shadowcolor)

                        draw.text((x - 1, y - 1),
                                  texto,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x + 1, y - 1),
                                  texto,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x - 1, y + 1),
                                  texto,
                                  font=font,
                                  fill=shadowcolor)
                        draw.text((x + 1, y + 1),
                                  texto,
                                  font=font,
                                  fill=shadowcolor)

                        draw.text((x, y), texto, font=font, fill=fillcolor)
                        text = text[xx + 1:len(text)]

                        y = y + 15

            draw.text((x - 1, y), text, font=font, fill=shadowcolor)
            draw.text((x + 1, y), text, font=font, fill=shadowcolor)
            draw.text((x, y - 1), text, font=font, fill=shadowcolor)
            draw.text((x, y + 1), text, font=font, fill=shadowcolor)

            draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
            draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
            draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
            draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)
            draw.text((x, y), text, font=font, fill=fillcolor)

            fname2 = "goldmeme.jpg"
            im.save(fname2)

            await ctx.channel.send(file=discord.File('goldmeme.jpg'))
        else:
            await ctx.channel.send(
                "❌| You aren't allowed to use this command here")

    @commands.command(name='senpai',
                      help="Find out how much of a senpai you are")
    async def cmd(self, ctx, user=''):
        if (user == ''):
            if (str(ctx.message.author.id) == GOLD_ID):
                await ctx.channel.send(ctx.message.author.name +
                                       "'s senpai meter: ♾️ " +
                                       "\nThere can only be one true senpai😩👌")
                return

            n = random.randrange(1, 100, 2)

            if (n < 30):
                await ctx.channel.send(ctx.message.author.name +
                                       "'s senpai meter: " + str(n) +
                                       "\nMore like a kouhai🚮")

            elif (n < 65):
                await ctx.channel.send(
                    ctx.message.author.name + "'s senpai meter: " + str(n) +
                    "\nNot senpai enough to make me wanna be noticed.")

            else:
                embed = discord.Embed(color=0x50bdfe)
                embed.set_author(name="Best senpai")
                embed.set_thumbnail(
                    url=
                    'https://media1.tenor.com/images/ed592e883d3bfd53476f6c34c412e2ad/tenor.gif?itemid=5645928'
                )
                await ctx.channel.send(ctx.message.author.name +
                                       "'s senpai meter: " + str(n) + "\n")
                await ctx.send(embed=embed)
        else:
            temp = re.findall(r'\d+', user)
            res = list(map(int, temp))
            id = 0
            for i in range(len(res)):
                id = (id * 10) + res[i]
            sid = str(id)

            usrobj = discord.utils.find(lambda m: m.id == id,
                                        ctx.message.channel.guild.members)
            if (not usrobj):
                await ctx.channel.send("The specified user is not found!")
                return

            if (sid == GOLD_ID):
                await ctx.channel.send(usrobj.name + "'s senpai meter: ♾️ " +
                                       "\nThere can only be one true senpai😩👌")
                return

            n = random.randrange(1, 100, 2)

            if (n < 30):
                await ctx.channel.send(usrobj.name + "'s senpai meter: " +
                                       str(n) + "\nMore like a kouhai🚮")

            elif (n < 65):
                await ctx.channel.send(
                    usrobj.name + "'s senpai meter: " + str(n) +
                    "\nNot senpai enough to make me wanna be noticed.")

            else:
                embed = discord.Embed(color=0x50bdfe)
                embed.set_author(name="Best senpai")
                embed.set_thumbnail(
                    url=
                    'https://media1.tenor.com/images/ed592e883d3bfd53476f6c34c412e2ad/tenor.gif?itemid=5645928'
                )
                await ctx.channel.send(usrobj.name + "'s senpai meter: " +
                                       str(n) + "\n")
                await ctx.send(embed=embed)

    @commands.command(name="owo",
                      help="sound like a furry",
                      aliases=["owofy", "owoify"])
    async def owo(self, ctx, *, str=""):
        str = str.lower()

        if str != "":
            owostr = str.replace("o", "owo")
            owostr = owostr.replace("u", "uwu")

            owostr = owostr.replace("you", "chu")
            owostr = owostr.replace("ove", "uv")
            owostr = owostr.replace("no", "nu")

            owostr = owostr.replace("r", "w")
            owostr = owostr.replace("l", "w")
            owostr = owostr.replace("th", "ff")

            owoappend = ["òwó", "owo", "UwU", "uwu", "d-daddy", "qwq"]
            owoemotes = ["(≧∀≦)", "(⋟﹏⋞)", "(＾▽＾)", "<3", "（*＾3＾）"]

            s = owostr[0]
            owostr = owostr.replace(s, (s + "-" + s), 1)

            owostr = random.choice(
                owoappend) + " " + owostr + " " + random.choice(
                    owoemotes) + " ~"
            await ctx.send(owostr)
        else:
            await ctx.send("e-entew a textw to owoify UwU (⋟﹏⋞)")

    @commands.command(name='gamerpoints', help="tells you your gamer points")
    async def gamerpoints(self, ctx, user=''):
        if (user == ''):
            if (str(ctx.message.author.id) == PRAX_ID):
                await ctx.channel.send(ctx.message.author.name +
                                       "'s gamer points: ♾️ " +
                                       "\nOfc he's the best gamer in town😳")
                return

            n = random.randrange(1, 100, 2)

            if (n < 30):
                await ctx.channel.send(ctx.message.author.name +
                                       "'s gamer points: " + str(n) +
                                       "\nsmh git gud nub")

            elif (n < 65):
                await ctx.channel.send(
                    ctx.message.author.name + "'s gamer points: " + str(n) +
                    "\nThats alright I guess, stilla nub tho")

            else:
                await ctx.channel.send(ctx.message.author.name +
                                       "'s gamer points: " + str(n) +
                                       "\npro gamer 😩")
        else:
            temp = re.findall(r'\d+', user)
            res = list(map(int, temp))
            id = 0
            for i in range(len(res)):
                id = (id * 10) + res[i]
            sid = str(id)

            usrobj = discord.utils.find(lambda m: m.id == id,
                                        ctx.message.channel.guild.members)
            if (not usrobj):
                await ctx.channel.send("The specified user is not found!")
                return

            if (sid == PRAX_ID):
                await ctx.channel.send(usrobj.name + "'s gamer points: ♾️ " +
                                       "\nOfc he's the best gamer in town😳")
                return

            n = random.randrange(1, 100, 2)

            if (n < 30):
                await ctx.channel.send(usrobj.name + "'s gamer points: " +
                                       str(n) + "\nsmh git gud nub")

            elif (n < 65):
                await ctx.channel.send(
                    usrobj.name + "'s gamer points: " + str(n) +
                    "\nThats alright I guess, stilla nub tho")

            else:
                await ctx.channel.send(usrobj.name + "'s gamer points: " +
                                       str(n) + "\npro gamer 😩")


def setup(bot):
    bot.add_cog(Fun(bot))