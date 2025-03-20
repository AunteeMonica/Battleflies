# from cogs.modules.battlefly_functionality import battleflyFunctionality
from cogs.battleflybot_cog import BattleflyBotCog
from cogs.logic.inventory_logic import InventoryLogic
from discord.ext import commands
from modules.battleflybot_exceptions import (
    CatchCooldownIncompleteException,
    HigherPageSpecifiedException,
    HigherReleaseQuantitySpecifiedException,
    NoEggCountException,
    NotEnoughExchangebattleflyQuantityException,
    NotEnoughExchangebattleflySpecifiedException,
    NotEnoughCocoonQuantityException,
    PageQuantityTooLow,
    ReleaseQuantityTooLow,
    TooManyExchangebattleflySpecifiedException,
    UnregisteredAllyException,
)


class InventoryCommands(BattleflyBotCog):

    def __init__(self, bot):
        super().__init__()
        self.inventory_logic = InventoryLogic(bot)

    @commands.command(name='catch_old', aliases=['c'], pass_context=True)
    async def catch_old(self, ctx: commands.Context):
        """
        Catches a random Battlefly and gives it to the Ally
        """
        try:
            await self.inventory_logic.catch_battlefly(ctx)
        except CatchCooldownIncompleteException as e:
            await self.catch_cooldown_incomplete_msg(ctx, e)

    @commands.command(name='inv', aliases=['i'], pass_context=True)
    async def pinventory(
        self,
        ctx: commands.Context,
        page: int = commands.parameter(
            description="The @-mention of the user on discord.",
            default=1
        )
    ):
        """
        Displays the Ally's Battlefly inventory
        """
        try:
            if page < 1:
                raise PageQuantityTooLow()
            embed_msg = await self.inventory_logic.build_pinventory_msg(ctx, page)
            await ctx.send(embed=embed_msg)
        except HigherPageSpecifiedException as e:
            await self.higher_page_specified_msg(ctx, e)
        except PageQuantityTooLow:
            await self.page_quantity_too_low_msg(ctx)
        except UnregisteredAllyException:
            await self.unregistered_ally_msg(ctx)

    @commands.command(name='release', aliases=['r'], pass_context=True)
    async def release(
        self,
        ctx: commands.Context,
        battlefly_number: int = commands.parameter(
            description="The number of the Battlefly in your inventory"
        )
    ):
        """
        Allows players to release a Battlefly by its number in the inventory.
        """
        user_id = str(ctx.author.id)

        # Check if the player has an inventory
        if user_id not in self.inventory_logic.battlefly_inventory or not self.inventory_logic.battlefly_inventory[user_id]:
            await ctx.send(f"📭 {ctx.author.mention}, your inventory is empty! Nothing to release.")
            return

        # Validate number input
        if battlefly_number < 1 or battlefly_number > len(self.inventory_logic.battlefly_inventory[user_id]):
            await ctx.send(f"⚠️ {ctx.author.mention}, invalid Battlefly number! Use `!inv` to see your numbered list.")
            return

        # Remove the selected Battlefly
        removed_battlefly = self.inventory_logic.battlefly_inventory[user_id].pop(battlefly_number - 1)
        self.inventory_logic.save_inventory()

        await ctx.send(f"😢 {ctx.author.mention} released **{removed_battlefly['name']}** ({removed_battlefly['type']}) back into the wild!")

    @commands.command(name='eggs', aliases=['e'], pass_context=True)
    async def eggs(self, ctx: commands.Context) -> None:
        """
        Gets the number of eggs that the Ally has
        """
        try:
            embed_msg = await self.inventory_logic.build_eggs_msg(ctx)
            await ctx.send(embed=embed_msg)
        except UnregisteredAllyException:
            await self.unregistered_ally_msg()

    @commands.command(name='hatch', aliases=['h'], pass_context=True)
    async def hatch(
        self,
        ctx: commands.Context,
        special_egg: str = commands.parameter(
            description="Specify 'm' to hatch a special egg if you have one",
            default=''
        )
    ):
        """
        Hatches an egg from your inventory
        """
        try:
            await self.inventory_logic.hatch_egg(ctx, special_egg)
        except NoEggCountException as e:
            await self.no_egg_count_msg(ctx, e)
        except UnregisteredAllyException:
            await self.unregistered_ally_msg(ctx)

    @commands.command(name='exchange', pass_context=True)
    async def exchange(
        self,
        ctx: commands.Context,
        *args: str
    ) -> None:
        """
        Exchanges 5 Battleflies for a Battlefly with a modified chance rate

        Example usage:
        !exchange pikachu pikachu charizard squirtle bulbasaur
        """
        try:
            await self.inventory_logic.exchange_battlefly(ctx, *args)
        except NotEnoughExchangebattleflyQuantityException:
            await self.not_enough_exchange_battlefly_quantity_msg(ctx)
        except NotEnoughExchangebattleflySpecifiedException:
            await self.not_enough_exchange_battlefly_specified_msg(ctx)
        except TooManyExchangebattleflySpecifiedException:
            await self.too_many_exchange_battlefly_specified_msg(ctx)
        except UnregisteredAllyException:
            await self.unregistered_ally_msg(ctx)

    @commands.command(name='open', aliases=['o'], pass_context=True)
    async def open(
        self,
        ctx: commands.Context,
        cocoon: str = commands.parameter(
            description="Specify either a 'bronze', 'silver', or 'gold' cocoon to open"
        )
    ):
        """
        Opens a specified cocoon in the inventory
        """
        try:
            embed_msg = await self.inventory_logic.open_cocoon(ctx, cocoon)
            await ctx.send(embed=embed_msg)
        except NotEnoughCocoonQuantityException as e:
            await self.not_enough_cocoon_quantity_msg(ctx, e)
        except UnregisteredAllyException:
            await self.unregistered_ally_msg(ctx)

    @commands.command(name='cocoons', aliases=['l'], pass_context=True)
    async def cocoons(self, ctx: commands.Context):
        """
        Displays the number of cocoons the Ally has
        """
        try:
            embed_msg = await self.inventory_logic.display_cocoon_inventory(ctx)
            await ctx.send(embed=embed_msg)
        except UnregisteredAllyException:
            await self.unregistered_ally_msg(ctx)
