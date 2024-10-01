import discord, asyncio, nest_asyncio
from discord.ext import commands
import sys
import os
import psutil
from dotenv import load_dotenv

# Load Secrets
load_dotenv()
MY_GUILD = discord.Object(id=os.environ['GUILD']) # Your Guild/Server ID
TOKEN = os.environ['TOKEN']  # Always keep your token secure!
# TOKEN = 'your token' # Use this if .env doesn't work
APPLICATION_ID = os.environ['APP_ID'] # Your application ID

# psutil used to run bot on REALTIME on windows - used if it stutters while playing music 
# p = psutil.Process(os.getpid())
# p.nice(psutil.REALTIME_PRIORITY_CLASS)

# Get the directory of the currently running script
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

# Change the current working directory to the script's directory
os.chdir(script_directory)

# Print the new current working directory
print("Current working directory set to:", os.getcwd())

# Import the music cog
from cog import MusicCog

nest_asyncio.apply()

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True  # Para gerenciar o estado do voice channel
intents.messages = True
intents.message_content = True

# Create the bot instance with the specified intents and application_id
bot = commands.Bot(command_prefix="!", intents=intents, application_id=APPLICATION_ID)

# Remove default help command
bot.remove_command("help")


# In this basic example, we just synchronize the app commands to one guild.
# Instead of specifying a guild to every command, we copy over our global commands instead.
# By doing so, we don't have to wait up to an hour until they are shown to the end-user.
async def setup_hook():
    # This copies the global commands over to your guild.
    bot.tree.copy_global_to(guild=MY_GUILD)
    await bot.tree.sync(guild=MY_GUILD)
    print("Comandos sincronizados.")


async def main():
    print("Iniciando o bot...")
    await bot.add_cog(MusicCog(bot))
    print("Cog adicionado.")
    await MusicCog.clean_temp(bot)
    bot.setup_hook = setup_hook
    await bot.run(TOKEN)


# Run the bot
asyncio.run(main())
