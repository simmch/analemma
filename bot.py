import os
from dotenv import load_dotenv
from interactions import Client, ActionRow, Button, ButtonStyle, Intents, const, Status, Activity, listen, slash_command, global_autocomplete, InteractionContext, SlashCommandOption, OptionType, slash_default_member_permission, SlashCommandChoice, context_menu, CommandType, Permissions, cooldown, Buckets, Embed, AutocompleteContext, slash_option
from ai import run_search

guild_ids = None
guild_id = None
guild_channel = None

bot = Client(intents=Intents.ALL, sync_interactions=True, send_command_tracebacks=False)

load_dotenv()

def load(ctx, extension):
   bot.load_extension(f'cogs.{extension}')

def unload(ctx, extension):
   bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
   if filename.endswith('.py'):
      # :-3 removes .py from filename
      bot.load_extension(f'cogs.{filename[:-3]}')


if os.environ["env"] == "production":
   guild_id = 968404015912214539
   guild_channel = 957061470192033812
else:
   guild_ids = [968404015912214539]
   guild_id = 968404015912214539
   guild_channel = 962580388432195595


@listen()
async def on_ready():
   server_count = len(bot.guilds)
   await bot.change_presence(status=Status.ONLINE, activity=Activity(name=f"In Looters Bay 🌍", type=1))
   print("Bot is running")


@slash_command(description="Ask Analemma a question", options=[
    SlashCommandOption(name="question", description="The question you want to ask", type=OptionType.STRING, required=True)
], scopes=guild_ids)
async def ask(ctx, question: str):
   await ctx.defer()
   response = run_search(question)
   await ctx.send("You are asking the wrong questions." if response == "" else response)
   return





        



if os.environ["env"] == "production":
   DISCORD_TOKEN = os.environ['PRODUCTION_DISCORD_TOKEN']
else:
   DISCORD_TOKEN = os.environ['TEST_DISCORD_TOKEN']


bot.start(DISCORD_TOKEN)