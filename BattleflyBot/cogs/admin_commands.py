# from modules.battlefly_functionality import battleflyFunctionality
from cogs.battleflybot_cog import BattleflyBotCog
from cogs.logic.admin_logic import AdminLogic
from discord.ext import commands
from modules.battleflybot_exceptions import (
    HigherReleaseQuantitySpecifiedException,
    CocoonDoesNotExistException,
    NotEnoughCocoonQuantityException,
    BattleflyDoesNotExistException,
    UnregisteredAllyException
)
from utils.utils import format_shiny_battlefly_name, is_name_shiny

class AdminCommands(BattleflyBotCog):

    def __init__(self, bot):
        super().__init__()
        self.admin_logic = AdminLogic(bot)

    @commands.command(name='give', pass_context=True, hidden=True)
    @commands.has_role('battleflyBot Admin')
    async def give(
        self,
        ctx: commands.Context,
        user_id: int = commands.parameter(
            description="ID of the Ally to give a battlefly to"
        ),
        battlefly_name: str = commands.parameter(
            description="Name of the battlefly to give"
        ),
        shiny: str = commands.parameter(
            description="Specify 's' or not to give a shiny battlefly",
            default=''
        )
    ) -> None:
        """
        Gives a battlefly to an Ally (admin only command).
        """
        try:
            is_shiny = False
            if shiny == 's':
                is_shiny = True
            str_user_id = str(user_id)
            await self.admin_logic.give_battlefly(
                str_user_id,
                battlefly_name,
                is_shiny
            )
            formatted_battlefly_name = battlefly_name.title()
            if is_shiny:
                formatted_battlefly_name = "(Shiny) " + formatted_battlefly_name
            await ctx.send(f"{ctx.message.author.mention} gave a"
                           f" **{formatted_battlefly_name}** to <@{str_user_id}>")
        except BattleflyDoesNotExistException as e:
            await self.battlefly_does_not_exist_msg(ctx, e)

    @commands.command(name='delete', pass_context=True, hidden=True)
    @commands.has_role('battleflyBot Admin')
    async def delete(
        self,
        ctx: commands.Context,
        user_id: int = commands.parameter(
            description="ID of the Ally to remove a battlefly from"
        ),
        battlefly_name: str = commands.parameter(
            description="Name of the battlefly to delete"
        )
    ) -> None:
        """
        Deletes a battlefly from an Ally's collection (admin only command).
        """
        try:
            str_user_id = str(user_id)
            formatted_battlefly_name = battlefly_name.lower()
            await self.admin_logic.delete_battlefly(str_user_id, formatted_battlefly_name)
            if is_name_shiny(battlefly_name):
                formatted_battlefly_name = format_shiny_battlefly_name(battlefly_name)
            else:
                formatted_battlefly_name = formatted_battlefly_name.title()
            await ctx.send(f"{ctx.message.author.mention} deleted a"
                           f" **{formatted_battlefly_name}** from Ally"
                           f" <@{str_user_id}>")
        except UnregisteredAllyException as e:
            await self.unregistered_ally_admin_msg(ctx, e)
        except HigherReleaseQuantitySpecifiedException as e:
            await self.higher_quantity_specified_msg(ctx, e)
        except BattleflyDoesNotExistException as e:
            await self.battlefly_does_not_exist_msg(ctx, e)

    @commands.command(name='givecocoon', pass_context=True, hidden=True)
    @commands.has_role('battleflyBot Admin')
    async def givecocoon(
        self,
        ctx: commands.Context,
        user_id: int = commands.parameter(
            description="ID of the Ally to give a cocoon to"
        ),
        cocoon: str = commands.parameter(
            description="Specify either 'bronze', 'silver', or 'gold' cocoon"
        )
    ) -> None:
        """
        Gives an Ally a specified cocoon.
        """
        try:
            str_user_id = str(user_id)
            formatted_cocoon = cocoon.lower()
            await self.admin_logic.give_cocoon(str_user_id, formatted_cocoon)
            await ctx.send(f"{ctx.message.author.mention} gave a"
                           f" **{formatted_cocoon.title()}** cocoon"
                           f" to Ally <@{str_user_id}>")
        except CocoonDoesNotExistException as e:
            await self.cocoon_does_not_exist_msg(ctx, e)

    @commands.command(name='deletecocoon', pass_context=True, hidden=True)
    @commands.has_role('battleflyBot Admin')
    async def deletecocoon(
        self,
        ctx: commands.Context,
        user_id: int = commands.parameter(
            description="ID of the Ally to remove a cocoon from"
        ),
        cocoon: str = commands.parameter(
            description="Specify either 'bronze', 'silver', or 'gold' cocoon"
        )
    ) -> None:
        """
        Deletes a cocoon from an Ally's inventory.
        """
        try:
            str_user_id = str(user_id)
            formatted_cocoon = cocoon.lower()
            await self.admin_logic.delete_cocoon(str_user_id, formatted_cocoon)
            await ctx.send(f"{ctx.message.author.mention} deleted a"
                           f" **{formatted_cocoon.title()}** cocoon from"
                           f" Ally <@{str_user_id}>")
        except UnregisteredAllyException as e:
            await self.unregistered_ally_admin_msg(ctx, e)
        except CocoonDoesNotExistException as e:
            await self.cocoon_does_not_exist_msg(ctx, e)
        except NotEnoughCocoonQuantityException as e:
            await self.not_enough_cocoon_quantity_msg(ctx, e)
