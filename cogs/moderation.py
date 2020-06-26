import os
import time
import json
import math
import discord
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()

ANTISPAM_BOT_ID = str(os.getenv('ANTISPAM_BOT_ID'))
LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID'))

dirname = os.path.dirname(__file__)
data_filename = os.path.join(dirname, '../data.json')


def numOfDays(date1):
    return ((datetime.today()) - date1).days


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if ((message.content.lower() == "t!info"
             or message.content.lower() == "t!profile")
                and message.channel.name == "get-verified"):
            role2 = discord.utils.get(message.author.guild.roles, name="MOD")

            member = message.author

            role1 = discord.utils.get(member.guild.roles,
                                      name="🔱⠀Arcadia Citizen⠀🔱")
            a = list()

            with open(data_filename) as f:
                d = json.load(f)
                for i in d["xp"]:
                    if (int(i["count"]) > 5):
                        a.append(i["id"])
            if (role1 in member.roles):
                await message.channel.send("You already have the role 👍")
                return

            if (member.id in a):
                await message.channel.send(
                    "You've been softbanned and thus cant pass!")
                return

            dt = str(message.author.created_at)
            date1 = message.author.created_at
            await message.channel.send("Acc. created on: " + str(dt))
            if (numOfDays(date1) > 30):
                await message.channel.send("Verified 👍")
                await member.add_roles(role1)
                time.sleep(5)

                await message.channel.purge(limit=None,
                                            check=lambda msg: not msg.pinned)
            else:
                await message.channel.send("account is not even a month old!")
                await message.channel.send("{} verify this kid.".format(
                    role2.mention))

        if ('mute' in message.content
                and message.author.id == ANTISPAM_BOT_ID):
            user = message.mentions[0]
            id = user.id
            print(message.mentions)
            role = discord.utils.get(user.guild.roles, name="Muted")

            p = 0

            with open(data_filename) as f:
                d = json.load(f)

                if (int(id) in d["spam"]):
                    p = 1

            if (p == 1):
                await message.channel.send("chook chook")

            if (p == 1 and role in user.roles):
                await user.remove_roles(role)
                await message.channel.send("***Speak {}***".format(user.name))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"**Command is on cooldown. Retry after {math.ceil(error.retry_after)}s**"
            )

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "**You dont have the permissions to run this command**")

        else:
            raise error

    @commands.command(name='devreset', help="seekrit")
    async def devdump(self, ctx):
        if (ctx.message.author.id == 489658911792562186):
            with open(data_filename, 'w') as f:
                d = {"xp": [], "emotes": []}
                json.dump(d, f)
                await ctx.message.channel.send("***done...***")
        else:
            await ctx.message.channel.send("go away pl0z")

    @commands.command(name='softban',
                      help='removes the citizen role of a user')
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *msg):

        if member is None:
            await ctx.send("**Please mention a member to softban**")
            return

        role1 = discord.utils.get(member.guild.roles,
                                  name="🔱⠀Arcadia Citizen⠀🔱")
        role2 = discord.utils.get(member.guild.roles, name="MOD")

        if (role2 in member.roles):
            await member.remove_roles(role2)

        await member.remove_roles(role1)
        await ctx.message.channel.send(
            "✅ ***{} has been yeeted away***".format(member.name))

        ch = self.bot.get_channel(LOG_CHANNEL_ID)
        m = ''.join(msg)
        if (m == ''):
            m = "None specified."

        embed = discord.Embed(title="{} has been softbanned!".format(
            member.name),
                              color=0x00ff00)
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="Softbanned by:",
                        value=ctx.message.author.name,
                        inline=False)
        embed.add_field(name="Reason:", value=m, inline=False)
        embed.set_thumbnail(url=member.avatar_url)

        await ch.send(embed=embed)

    @commands.command(name='spamlist', help='allows people to spam')
    @commands.has_any_role('SENIOR MOD', 'Ninja', 'ARCADIA ADMINS', 'MOD')
    async def spamlist(self, ctx, member: discord.Member):
        id = member.id
        d = {}

        with open(data_filename) as f:
            d = json.load(f)
            if (int(id) in d["spam"]):
                await ctx.message.channel.send(
                    "*** {} is already in the list..***".format(member.name))
                return
            d["spam"].append(id)

        with open(data_filename, 'w') as f:
            json.dump(d, f)

        await ctx.message.channel.send(
            "*** {} has been added to the list of people allowed to spam!***".
            format(member.name))

    @commands.command(name="spamremove", help="removes member from spam list")
    @commands.has_any_role('SENIOR MOD', 'Ninja', 'ARCADIA ADMINS', 'MOD')
    async def spamremove(self, ctx, user: discord.Member):
        id = user.id
        d = {}

        with open(data_filename) as f:
            d = json.load(f)

            if (id in d["spam"]):
                d["spam"].remove(id)
                await ctx.message.channel.send(
                    "*** {} has been removed from the list!***".format(
                        user.name))
            else:
                await ctx.message.channel.send(
                    "*** {} is not in the list.***".format(user.name))

        with open(data_filename, 'w') as f:
            json.dump(d, f)

    @commands.command(name='displayspam', help='displays spam list')
    async def displayspam(self, ctx):
        s = ""
        n = 1

        with open(data_filename) as f:
            d = json.load(f)

            for i in d["spam"]:
                member = self.bot.get_user(i)
                s = s + "{}. {} \n".format(n, member.name)

                n += 1

        embed = discord.Embed(title="Spam List                      ".format(
            member.name),
                              color=0x00ff00)
        embed.description = s
        await ctx.message.channel.send(embed=embed)

    @commands.command(name='emoteDataClear', help='clears recorded emote data')
    async def say(self, ctx):
        d = {"money": [], "emotes": []}
        with open(data_filename, "w") as f:
            json.dump(d, f)
        await ctx.message.channel.send(
            "```All tracked emote usage data has been cleared```")


def setup(bot):
    bot.add_cog(Moderation(bot))