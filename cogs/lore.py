import uuid
import utilities.timestamps as timestamps
import classes.lore_class as lore
from interactions import Modal, ParagraphText, ShortText, SlashContext, ModalContext, Client, ActionRow, Button, ButtonStyle, Intents, listen, slash_command, InteractionContext, SlashCommandOption, OptionType, slash_default_member_permission, SlashCommandChoice, context_menu, CommandType, Permissions, cooldown, Buckets, Embed, Extension
import vectorsearch

class Lore(Extension):
    def __init__(self, bot):
        self.bot = bot

    @listen()
    async def on_ready(self):
        print("Lore cog is ready")

    @slash_command(name="newentry", description="Add Lore to the bot")
    async def newentry(self, ctx: SlashContext):
        try:
            _uuid = str(uuid.uuid4())
            lore_modal = Modal(
                ShortText(label="Lore Title", custom_id=f"short_text-{_uuid}"),
                ParagraphText(label="Lore Description", custom_id=f"long_text-{_uuid}"),
                title="New Lore",
            )
            await ctx.send_modal(modal=lore_modal)
            modal_ctx: ModalContext = await self.bot.wait_for_modal(lore_modal)

            lore_title = modal_ctx.responses[f"short_text-{_uuid}"]
            lore_description = modal_ctx.responses[f"long_text-{_uuid}"]
            # Removing all spaces
            lore_title_no_spaces = lore_title.replace(" ", "")
            lore_description_no_spaces = lore_description.replace(" ", "")
            writer_id = str(ctx.author.id)
            now = timestamps.get_timestamp()
            new_lore = lore.Lore(lore_title, lore_description, writer_id, now, lore_title_no_spaces, lore_description_no_spaces)
            new_lore.save()
            response = vectorsearch.add_embedding(lore_title)
            if response:
                await modal_ctx.send(f"New lore about **{lore_title}** has been added to the dnd database. Embedding has been added.")
            else:
                await modal_ctx.send(f"New lore about **{lore_title}** has been added to the dnd database. However, embedding was not added. Please contact the developer.")
            return
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("An error occurred while adding the lore. Please try again.")
            return
        



def setup(bot):
    Lore(bot)