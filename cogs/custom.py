import os
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands
from firebase_admin import firestore
from tatsumaki.wrapper import ApiWrapper

load_dotenv()

ARCADIA_ID = int(os.getenv('ARCADIA_ID'))
TATSUMAKI_KEY = str(os.getenv('TATSUMAKI_KEY'))

db = firestore.client()

tatsu = ApiWrapper(TATSUMAKI_KEY)


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        channel = msg.channel
        msg = msg.content
        if msg.startswith("+"):
            command = msg[1:]

            doc_ref = db.collection('custom-command').where(
                'name', '==', command).limit(1)
            docs = doc_ref.stream()
            doc = {}
            for document in docs:
                doc = document.to_dict()

            if doc != {}:
                title = doc["title"]
                imgUrl = doc["image"]

                embed = discord.Embed(title=title, color=0x00ff00)
                embed.set_image(url=imgUrl)
                await channel.send(embed=embed)

    @commands.command(name="custom", help="add a custom command for yourself!")
    async def get(self, ctx):
        guild_id = ARCADIA_ID
        user_id = ctx.author.id
        data = await tatsu.get_user_stats(guild_id, user_id)

        cmd = ""
        title = ""
        imgUrl = ""

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        if int(data['score']) < 234000:
            await ctx.send(
                f"**You need at least 234k tatsumaki XP in this guild to run this command!**\n __Your score: {data['score']}__"
            )
        else:
            doc_ref = db.collection("custom-command").document(str(user_id))
            doc = doc_ref.get()

            if doc.exists:
                await ctx.send(
                    "__You already have a custom command registered__")
            else:
                await ctx.send(
                    "__Type 'end' at any point to terminate process__\n**Enter the name of your command**"
                )

                try:
                    cmd = await self.bot.wait_for('message',
                                                  timeout=60.0,
                                                  check=check)
                except asyncio.TimeoutError:
                    await ctx.message.channel.send(
                        'Event cancelled as no response recieved')
                else:
                    cmd = cmd.content

                    if (cmd.lower() == 'end'):
                        await ctx.send("__Process terminated__")
                        return

                    docs = db.collection('custom-command').where(
                        "name", "==", cmd).limit(1).stream()
                    doc = {}

                    for i in docs:
                        doc = i.to_dict()

                    if doc != {}:
                        await ctx.send("**Command already exists**")
                        return

                await ctx.send("**Enter a title you want displayed**")

                try:
                    title = await self.bot.wait_for('message',
                                                    timeout=60.0,
                                                    check=check)
                except asyncio.TimeoutError:
                    await ctx.message.channel.send(
                        'Event cancelled as no response recieved')
                else:
                    title = title.content
                    if (title.lower() == 'end'):
                        await ctx.send("__Process terminated__")
                        return

                await ctx.send("**Enter URL of an image u want displayed**")

                flag = True

                while flag:
                    try:
                        imgUrl = await self.bot.wait_for('message',
                                                         timeout=60.0,
                                                         check=check)
                    except asyncio.TimeoutError:
                        await ctx.message.channel.send(
                            'Event cancelled as no response recieved')
                    else:
                        if imgUrl.content.lower() == 'end':
                            await ctx.send("__Process terminated__")
                            return
                        elif not (imgUrl.content.startswith('http')):
                            await ctx.send(
                                "__Not a valid URL, please enter a **Valid URL**__"
                            )
                        else:
                            imgUrl = imgUrl.content
                            flag = False

                await ctx.send("`HERES A PREVIEW-`")
                embed = discord.Embed(title=title, color=0x00ff00)
                embed.set_image(url=imgUrl)
                await ctx.message.channel.send(embed=embed)

                doc_ref.set({'name': cmd, 'title': title, 'image': imgUrl})

                await ctx.send("**☑️ COMMAND REGISTERED**")

    @commands.command(name="customlist",
                      help="displays a list of custom commands")
    async def listall(self, ctx):
        docs = db.collection('custom-command').stream()
        desc = ""

        for doc in docs:
            command = doc.to_dict()['name']
            desc += f"**+{command}**\n"
        desc += "\n-- Use +customhelp\n"

        embed = discord.Embed(title="List of all custom commands",
                              color=0x00ff00)
        embed.set_thumbnail(
            url=
            "https://images-ext-1.discordapp.net/external/sc3p-qOYB1jWwkFDfd4i6W7_r-lQP7o9rShmSlNT3zM/%3Fsize%3D256/https/cdn.discordapp.com/avatars/650969739107237900/8aa95ac0cf6413decdfd6c76e9c30f6e.png"
        )
        embed.description = desc
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="customupdate",
                      help="update a command registered by you")
    async def update(self, ctx):
        user_id = str(ctx.author.id)
        title = ""
        imgUrl = ""
        c = 0

        doc_ref = db.collection('custom-command').document(user_id)
        doc = doc_ref.get()

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        if doc.exists:
            await ctx.send(
                "__Type 'end' at any point to terminate process__\n__Type 'none' if u dont want to make any change to a field__\n**Enter the changed title**"
            )

            try:
                title = await self.bot.wait_for('message',
                                                timeout=60.0,
                                                check=check)
            except asyncio.TimeoutError:
                await ctx.message.channel.send(
                    'Event cancelled as no response recieved')
            else:
                title = title.content
                if title.lower() == 'end':
                    await ctx.send("__Process terminated__")
                    return
                elif title.lower() == 'none':
                    title = doc.to_dict()["title"]
                    c += 1

            await ctx.send("**Enter changed image URL**")

            flag = True

            while flag:
                try:
                    imgUrl = await self.bot.wait_for('message',
                                                     timeout=60.0,
                                                     check=check)
                except asyncio.TimeoutError:
                    await ctx.message.channel.send(
                        'Event cancelled as no response recieved')
                else:
                    if imgUrl.content.lower() == 'end':
                        await ctx.send("__Process terminated__")
                        return
                    elif imgUrl.content.lower() == 'none':
                        imgUrl = doc.to_dict()["image"]
                        c += 1
                        flag = False
                    elif not (imgUrl.content.startswith('http')):
                        await ctx.send(
                            "__Not a valid URL, please enter a **Valid URL**__"
                        )
                    else:
                        imgUrl = imgUrl.content
                        flag = False

            await ctx.send("`HERES A PREVIEW-`")
            embed = discord.Embed(title=title, color=0x00ff00)
            embed.set_image(url=imgUrl)
            await ctx.message.channel.send(embed=embed)

            if c != 2:
                doc_ref.update({'title': title, 'image': imgUrl})

            await ctx.send("**☑️ COMMAND UPDATED**")
        else:
            await ctx.send(
                "Huh? You dont even have a command registered dude <:w0t:725098388357644371>"
            )

    @commands.command(name="customdelete", help="delete your custom command")
    async def delete(self, ctx):
        user_id = str(ctx.author.id)
        choice = ""
        flag = True

        doc_ref = db.collection("custom-command").document(user_id)
        doc = doc_ref.get()

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        if doc.exists:
            await ctx.send(
                "**Are you sure you want to delete the command? (Y/N)**")
            while flag:
                try:
                    choice = await self.bot.wait_for('message',
                                                     timeout=60.0,
                                                     check=check)
                except asyncio.TimeoutError:
                    await ctx.send("Event cancelled as no response recieved")
                    return
                else:
                    choice = choice.content.lower()
                    if choice == 'n':
                        await ctx.send("**Process terminated**")
                        return
                    elif choice != 'y':
                        await ctx.send("**Invalid input. Try again-**")
                    else:
                        flag = False

            doc_ref.delete()

            await ctx.send("**☑️ COMMAND DELETED**")

        else:
            await ctx.send("DeLeTe mY c0MmaNd 🥴 go register one first lmao.")

    @commands.command(name="customhelp",
                      help="gives help message for using custom commands")
    async def help(self, ctx):
        desc = ""
        desc += "**+custom -** `Add a custom command (required Tatsu score > 234000)`\n"
        desc += "**+customlist -** `Lists all custom commands`\n"
        desc += "**+customupdate -** `Updates the title and image of your command`\n"
        desc += "**+customdelete -** `Deletes your custom command`\n"

        embed = discord.Embed(title="Custom commands help", color=0x00ff00)
        embed.description = desc

        await ctx.message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Custom(bot))