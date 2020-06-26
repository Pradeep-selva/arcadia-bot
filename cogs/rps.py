import os
import asyncio
import discord
from discord.ext import commands
from firebase_admin import firestore

db = firestore.client()


class Rps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rps", help="play rock,paper,scissor")
    async def rps(self, ctx, member: discord.Member = None):
        p1 = ctx.message.author
        p2 = member

        def check1(m):
            return m.author == p1 and m.channel != ctx.message.channel

        def check2(m):
            return m.author == p2 and m.channel != ctx.message.channel

        def checkopt(m):
            return m.author == p2 and m.channel == ctx.channel

        if member is None:
            await ctx.channel.send(
                "{0.mention} Please mention a user to play against!".format(p1)
            )
        elif p1 == p2:
            await ctx.channel.send(
                "Smh are you really going to play with yourself? 🤮 ")
        else:

            await ctx.channel.send(
                "{0.mention} Do you accept the challenge? (Y/N)".format(p2))
            choice = ""

            try:
                choice = await self.bot.wait_for('message',
                                                 timeout=60.0,
                                                 check=checkopt)
            except asyncio.TimeoutError:
                await ctx.message.channel.send(
                    'Event cancelled as no response recieved')
            else:
                if (choice.content.upper() == "Y"):
                    await ctx.channel.send("**Respond in your DM**")
                    await p1.send(
                        "**Choose between rock, paper and scissor(R/P/S)**")
                    await p2.send(f"*{p1} is choosing. please wait...*")

                    move1 = ""
                    move2 = ""
                    winner = p1
                    fail = ""
                    m1 = ""
                    m2 = ""
                    try:
                        move1 = await self.bot.wait_for('message',
                                                        timeout=30.0,
                                                        check=check1)
                    except asyncio.TimeoutError:
                        await p1.send("No response recieved")
                        fail = "y"
                    else:
                        move1 = move1.content.lower()

                    await p2.send(
                        "**Choose between rock, paper and scissor(R/P/S)**")

                    try:
                        move2 = await self.bot.wait_for('message',
                                                        timeout=30.0,
                                                        check=check2)
                    except asyncio.TimeoutError:
                        await p2.send("No response recieved")
                        fail = "y"
                    else:
                        move2 = move2.content.lower()

                    if (move1 == "" or move2 == ""):
                        fail = "y"

                    elif (move1 == "r" and move2 == "s"):
                        winner = p1
                    elif (move1 == "r" and move2 == "p"):
                        winner = p2
                    elif (move1 == "s" and move2 == "p"):
                        winner = p1
                    elif (move1 == "s" and move2 == "r"):
                        winner = p2
                    elif (move1 == "p" and move2 == "r"):
                        winner = p1
                    elif (move1 == "p" and move2 == "s"):
                        winner = p2
                    elif (move1 == move2):
                        winner = "tie"
                    else:
                        fail = "y"

                    if fail != "y":
                        if move1 == "r":
                            m1 = "rock"
                        elif move1 == "s":
                            m1 = "scissor"
                        elif move1 == "p":
                            m1 = "paper"

                        if move2 == "r":
                            m2 = "rock"
                        elif move2 == "s":
                            m2 = "scissor"
                        elif move2 == "p":
                            m2 = "paper"

                        desc = "{0.mention} won the game! What a pr0h 😩 ".format(
                            winner
                        ) if winner != "tie" else "{0.mention} and {1.mention} have tied with each other".format(
                            p1, p2)
                        desc = desc + "\n\n**Moves made:**\n{0.mention} picked `{1}`\n{2.mention} picked `{3}`".format(
                            p1, m1, p2, m2)

                        print(
                            '```p1:{}\np2:{}\nmove1:{}\nmove2:{}\nm1string:{}\nm2string{}\nwinner:{}```'
                            .format(p1, p2, move1, move2, m1, m2, winner))

                        embed = discord.Embed(
                            title="Rock,Paper,Scissors game result!",
                            description=desc,
                            color=0x00ff00)
                        if (winner != "tie"):
                            embed.set_thumbnail(url=winner.avatar_url)

                            doc_ref = db.collection(u'rps').document(
                                str(winner.id))
                            doc = doc_ref.get()

                            print(winner)

                            if doc.exists:
                                print(doc.to_dict())
                                doc_ref.update(
                                    {'points': firestore.Increment(1)})
                            else:
                                print(doc.to_dict())
                                doc_ref.set({
                                    u'points': 1,
                                    'name': winner.name
                                })

                        await ctx.channel.send(embed=embed)
                    else:
                        print(
                            '```p1:{}\np2:{}\nmove1:{}\nmove2:{}\nm1string:{}\nm2string{}\nwinner:{}```'
                            .format(p1, p2, move1, move2, m1, m2, winner))
                        await ctx.channel.send(
                            "**Challenge declined due to invalid responses/no responses**"
                        )

                elif (choice.content.upper() == "N"):
                    await ctx.channel.send("**Challenge has been declined!**")
                else:
                    await ctx.channel.send(
                        "**Challenge declined due to invalid input**")

    @commands.command(name="rpsscore", help="view your rps score")
    async def rpsscore(self, ctx, user: discord.Member = None):
        user_id = ctx.author.id
        author = ctx.author
        if user is not (None):
            user_id = user.id
            author = user

        doc = db.collection('rps').document(str(user_id)).get()

        if doc.exists:
            embed = discord.Embed(title="Your RPS Score: ", color=0x00ff00)
            desc = doc.to_dict()['points']
            embed.description = desc
            embed.set_thumbnail(url=author.avatar_url)
            await ctx.message.channel.send(embed=embed)
        else:
            await ctx.channel.send(
                "{0.mention}, No history of your matches has been found.".
                format(author))

    @commands.command(name="toprps", help="view the top 10 rps players")
    async def rpstop(self, ctx):
        docs_ref = db.collection('rps').order_by(
            'points', direction=firestore.Query.DESCENDING).limit(10)
        docs = docs_ref.stream()
        desc = ""
        c = 1

        for doc in docs:
            name = doc.to_dict()['name']
            points = doc.to_dict()['points']
            desc += f'**{c}. {name} -** {points} \n'
            c += 1

        embed = discord.Embed(title="Top 10 users on RPS scoreboard",
                              color=0x1FEAEA)
        embed.description = desc

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Rps(bot))
