import os
from dotenv import load_dotenv
from interactions.ext.paginators import Paginator
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


activity_txt = "In Loota's Bae 🌍"

if os.environ["env"] == "production":
   guild_id = 968404015912214539
   guild_channel = 957061470192033812
else:
   guild_ids = [968404015912214539]
   guild_id = 968404015912214539
   guild_channel = 962580388432195595
   activity_txt = "Testing some code"


@listen()
async def on_ready():
   server_count = len(bot.guilds)
   await bot.change_presence(status=Status.ONLINE, activity=Activity(name=f"{activity_txt}", type=1))
   print("Bot is running")


@slash_command(description="Ask the lore bot a question", options=[
    SlashCommandOption(name="question", description="The question you want to ask", type=OptionType.STRING, required=True)
], scopes=guild_ids)
async def ask(ctx, question: str):
   await ctx.defer()
   try:
      response = await run_search(question)
      # embedVar = Embed(title=f"{question}", color=0x00ff00)
      # embedVar.add_field(name="Answer", value=f"{response}", inline=False)
      # await ctx.send(embed=embedVar)
      embed_list = []  # This is where we'll store our embeds

      # Let's slice and dice
      for i in range(0, len(response), 1000):
         chunk = response[i:i+1000]  # Get a slice of 1000 chars
         embedVar = Embed(title=f"{question}", color=0x00ff00)
         embedVar.add_field(name="Answer", value=f"{chunk}", inline=False)
         embed_list.append(embedVar)  # Add our embed to the list
      paginator = Paginator.create_from_embeds(bot, *embed_list)
      paginator.show_select_menu = True
      await paginator.send(ctx)
      return
   except Exception as e:
      print(f"Error: {e}")
      await ctx.send("The lore bot is resting a bit. Please ask your question again.", ephemeral=True)
      return

@slash_command(description="Ask Analemma a question, text response only", options=[
    SlashCommandOption(name="question", description="The question you want to ask", type=OptionType.STRING, required=True)
], scopes=guild_ids)
@slash_default_member_permission(Permissions.ADMINISTRATOR)
async def asktextresponse(ctx, question: str):
   try:
      await ctx.defer()
      response = await run_search(question)
      await ctx.send(response, ephemeral=True)
      return
   except Exception as e:
      print(f"Error: {e}")
      await ctx.send("The lore bot is resting a bit. Please ask your question again.", ephemeral=True)
      return


if os.environ["env"] == "production":
   DISCORD_TOKEN = os.environ['PRODUCTION_DISCORD_TOKEN']
else:
   DISCORD_TOKEN = os.environ['TEST_DISCORD_TOKEN']


bot.start(DISCORD_TOKEN)