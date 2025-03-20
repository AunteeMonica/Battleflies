from discord.ext import commands

class CocoonCog(commands.Cog):
    def __init__(self):
        super().__init__()
        print(f"Added {type(self).__name__} Cog")

    async def post_cocoon_does_not_exist_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please specify a valid cocoon to open (**{str(e)}** does not exist).")

    async def post_not_enough_cocoon_quantity_msg(self, ctx: commands.Context, e: Exception) -> None:
        await ctx.send(f"{ctx.message.author.mention}, please make sure you have enough **{str(e)}** cocoons to open.")
