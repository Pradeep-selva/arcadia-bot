import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

# getting discord token
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# initialising firebase app
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './fbkey.json')
cred = credentials.Certificate(filename)
firebase_admin.initialize_app(cred)

intial_extensions = [
    'cogs.custom', 'cogs.fun', 'cogs.moderation', 'cogs.rps', 'cogs.stats',
    'cogs.utilities'
]

bot = commands.Bot(command_prefix='+', help_command=None)

# loading all cogs
if __name__ == '__main__':
    for extension in intial_extensions:
        print(f"{extension[5:]}.py loaded")
        bot.load_extension(extension)


@bot.event
async def on_ready():
    activity = discord.Game(name="+help")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print(f'{bot.user.name} has connected to Discord!')


bot.run(token, bot=True, reconnect=True)
