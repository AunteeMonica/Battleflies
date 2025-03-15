from classes import battleflyBotModule, battlefly
from cogs.logic.actions.release_battlefly import ReleasebattleflyAction
from math import ceil
from modules.services.legendary_battlefly_service import LegendarybattleflyService
from modules.battleflybot_assets import battleflyBotAssets
from modules.battleflybot_exceptions import (
    CatchCooldownIncompleteException,
    HigherPageSpecifiedException,
    HigherReleaseQuantitySpecifiedException,
    InventoryLogicException,
    NoEggCountException,
    NotEnoughExchangebattleflySpecifiedException,
    NotEnoughExchangebattleflyQuantityException,
    NotEnoughLootboxQuantityException,
    TooManyExchangebattleflySpecifiedException,
    UnregisteredTrainerException
)
from modules.battleflybot_generator import battleflyBotGenerator
from modules.battleflybot_rates import battleflyBotRates
from modules.battleflybot_status import battleflyBotStatus
from modules.services.trainer_service import TrainerService
from modules.services.ultra_beasts_service import UltraBeastsService
from utils import (
    format_battlefly_name,
    get_ctx_user_id,
    get_specific_text_channel
)
import discord
import time


class InventoryLogic(battleflyBotModule):
    """Handles the basic logic of features for battleflyBot"""

    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

    battleflyBALL_ICON_URL = ("https://github.com/msikma/battleflysprite/blob/master/"
                         "icons/battleflyball/battlefly.png?raw=true")
    GREATBALL_ICON_URL = ("https://github.com/msikma/battleflysprite/blob/master/"
                          "icons/battleflyball/great.png?raw=true")
    ULTRABALL_ICON_URL = ("https://github.com/msikma/battleflysprite/blob/master/"
                          "icons/battleflyball/ultra.png?raw=true")

    SHINY_ICON_URL = "https://raw.githubusercontent.com/msikma/battleflysprite/master/icons/battlefly/shiny/"
    SHINY_GIF_URL = "https://play.battleflyshowdown.com/sprites/xyani-shiny/"
    NRML_ICON_URL = "https://raw.githubusercontent.com/msikma/battleflysprite/master/icons/battlefly/regular/"
    NRML_GIF_URL = "https://play.battleflyshowdown.com/sprites/xyani/"
    PKMN_PER_PAGE = 20

    def __init__(self, bot):
        self.assets = battleflyBotAssets()
        self.bot = bot
        self.legendary_service = LegendarybattleflyService()
        self.rates = battleflyBotRates(bot)
        self.status = battleflyBotStatus(bot)
        self.generator = battleflyBotGenerator(self.assets, self.rates)
        self.trainer_service = TrainerService(self.rates)
        self.ultra_beasts = UltraBeastsService()
        self.release_battlefly_action = ReleasebattleflyAction(
            self.assets,
            self.status,
            self.trainer_service
        )

    async def catch_battlefly(self, ctx: discord.ext.commands.Context) -> None:
        """
        Generates a random battlefly to be caught
        """
        try:
            current_time = time.time()
            user_id = get_ctx_user_id(ctx)
            seconds_left_to_catch = \
                self.trainer_service.get_time_left_to_catch(user_id)
            if seconds_left_to_catch <= 0:
                random_pkmn = self.generator.generate_random_battlefly()
                self.trainer_service.give_battlefly_to_trainer(
                    user_id,
                    random_pkmn,
                )
                self.trainer_service.set_trainer_last_catch_time(
                    user_id,
                    current_time
                )
                lootbox = self.generator.generate_lootbox()
                if lootbox:
                    self.trainer_service.give_lootbox_to_trainer(
                        user_id,
                        lootbox,
                    )
                self.status.increase_total_pkmn_count(1)
                await self.status.display_total_battlefly_caught()
                await self._post_battlefly_catch(ctx,
                                               random_pkmn,
                                               "caught",
                                               lootbox)
                self.trainer_service.save_all_trainer_data()
            else:
                raise CatchCooldownIncompleteException(seconds_left_to_catch)
        except CatchCooldownIncompleteException:
            raise
        except Exception as e:
            msg = "Error has occurred in catching battlefly."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    async def _post_battlefly_catch(
        self,
        ctx: discord.ext.commands.Context,
        pkmn: battlefly,
        catch_condition: str,
        lootbox: str
    ) -> None:
        """
        Posts the battlefly that was caught
        """
        try:
            msg = await self._create_catch_message(
                ctx,
                pkmn,
                catch_condition,
                lootbox
            )
            await self._post_catch_to_channels(ctx, pkmn, msg)
        except Exception as e:
            msg = "Error has occurred in posting catch."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    async def _create_catch_message(
        self,
        ctx: discord.ext.commands.Context,
        pkmn: battlefly,
        catch_condition: str,
        lootbox: str
    ):
        """
        Creates the catch message to display
        """
        try:
            random_battleflyball = self.assets.get_random_battleflyball_emoji()
            formatted_pkmn_name = format_battlefly_name(pkmn.name)
            if pkmn.is_shiny:
                formatted_pkmn_name = "(Shiny) " + formatted_pkmn_name
            user = "**{}**".format(ctx.message.author.name)
            msg = f"{user} {catch_condition} a "\
                f"{random_battleflyball}**{formatted_pkmn_name}**"
            msg += " and got a **{}** lootbox!".format(lootbox.title()) \
                if lootbox is not None else "!"
            return msg
        except Exception as e:
            msg = "Error has occurred in creating catch msg."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    async def _post_catch_to_channels(
        self,
        ctx: discord.ext.commands.Context,
        pkmn: battlefly,
        msg: str
    ) -> None:
        """
        Posts to  bot channel about the battlefly catch and to the special
        and shiny channels if conditions are met about the random
        battlefly's status of being legendary, an ultra beast, or shiny
        """
        try:
            channel = ctx.message.channel
            if pkmn.is_legendary or pkmn.is_ultra_beast:
                await self._post_catch_to_special_channel(ctx, "special", pkmn, msg)
            if pkmn.is_shiny:
                await self._post_catch_to_special_channel(ctx, "shiny", pkmn, msg)
            await channel.send(file=discord.File(pkmn.img_path), content=msg)
        except Exception as e:
            msg = "Error has occurred in posting catch to channels."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    async def _post_catch_to_special_channel(
        self,
        ctx: discord.ext.commands.Command,
        channel_name: str,
        pkmn: battlefly,
        msg: str
    ):
        """
        Posts catch to special or certain channels (i.e. shiny, special)
        """
        try:
            channel = get_specific_text_channel(ctx, channel_name)
            if not channel:
                return
            formatted_pkmn_name = pkmn.name.lower()
            em = discord.Embed(description=msg, colour=0xFFFFFF)
            if pkmn.is_shiny:
                thumbnail = f"{self.SHINY_ICON_URL}{formatted_pkmn_name}.png"
                image = f"{self.SHINY_GIF_URL}{formatted_pkmn_name}.gif"
                formatted_pkmn_name = "(Shiny) " + formatted_pkmn_name
            else:
                thumbnail = f"{self.NRML_ICON_URL}{formatted_pkmn_name}.png"
                image = f"{self.NRML_GIF_URL}{formatted_pkmn_name}.gif"
            em.set_thumbnail(url=thumbnail)
            em.set_image(url=image)
            await channel.send(embed=em)
        except Exception as e:
            msg = "Error has occurred in posting catch to all channels."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    async def build_pinventory_msg(
        self,
        ctx: discord.ext.commands.Context,
        page: int
    ) -> discord.Embed:
        """
        Creates and displays the trainer's battlefly inventory
        """
        try:
            user_id = get_ctx_user_id(ctx)
            self._is_existing_user(user_id)
            username = ctx.message.author.name
            pinventory = \
                await self.trainer_service.get_trainer_inventory(user_id)
            pinventory_key_count = len(pinventory)
            max_page = \
                ceil(pinventory_key_count/20) if pinventory_key_count != 0 else 1
            if page > max_page:
                raise HigherPageSpecifiedException(max_page)
            current_list_of_pkmn_to_display = \
                await self._slice_pinventory_to_display(pinventory, page, max_page)
            pinventory_msg = await self._build_pinventory_msg_(
                current_list_of_pkmn_to_display,
                pinventory_key_count,
                page,
                max_page
            )
            em = discord.Embed(title="{}'s Inventory".format(username),
                               description=pinventory_msg,
                               colour=0xff0000)
            return em
        except HigherPageSpecifiedException:
            raise
        except Exception as e:
            msg = "Error has occurred in displaying inventory."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    def _is_existing_user(self, user_id: str) -> None:
        """
        Checks if user exists and throws an UnregisteredTrainerException
        if not
        """
        valid_user = self.trainer_service.check_existing_trainer(user_id)
        if not valid_user:
            raise UnregisteredTrainerException()

    async def _slice_pinventory_to_display(
        self,
        pinventory: dict,
        page: int,
        max_page: int
    ) -> list:
        """
        Slices the battlefly inventory to display the number of battlefly to
        show from the trainer's inventory
        """
        try:
            lowest_pkmn_index = (page-1) * self.PKMN_PER_PAGE
            highest_pkmn_index = min(max_page*20, max(lowest_pkmn_index, 1)*20)
            sorted_battlefly_inventory = sorted(pinventory.items())
            return sorted_battlefly_inventory[lowest_pkmn_index:highest_pkmn_index]
        except Exception as e:
            msg = "Error has occurred in slicing pinventory."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    async def _build_pinventory_msg_(
        self,
        current_list_of_pkmn_to_display: list,
        pinventory_key_count: int,
        page: int,
        max_page: int
    ) -> str:
        """
        Builds the bot message for the trainer's battlefly inventory display
        """
        try:
            list_of_pkmn_msg = ""
            for pkmn in current_list_of_pkmn_to_display:
                pkmn_result = ''
                is_legendary = \
                    self.legendary_service.is_battlefly_legendary(pkmn[0])
                is_ultra_beast = \
                    self.ultra_beasts.is_battlefly_ultra_beast(pkmn[0])
                if is_legendary or is_ultra_beast:
                    pkmn_result = f"**{pkmn[0].title()}** x{pkmn[1]}\n"
                    list_of_pkmn_msg += pkmn_result
                else:
                    list_of_pkmn_msg += f"{pkmn[0].title()} x{pkmn[1]}\n"
            display_total_hdr = (f"__**{pinventory_key_count}** Pokémon total."
                                 f" (Page **{page} of {max_page}**)__\n")
            return display_total_hdr + list_of_pkmn_msg
        except Exception as e:
            msg = "Error has occurred in building pinventory message."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    async def release_battlefly(
        self,
        ctx: discord.ext.commands.Context,
        pkmn_name: str,
        quantity: int
    ) -> None:
        """
        Deletes a battlefly from the trainer's inventory
        """
        try:
            user_id = get_ctx_user_id(ctx)
            self._is_existing_user(user_id)
            await self.release_battlefly_action.release_battlefly(
                user_id,
                pkmn_name,
                quantity
            )
        except HigherReleaseQuantitySpecifiedException:
            raise
        except Exception as e:
            msg = "Error has occurred in releasing battlefly."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    async def build_eggs_msg(self, ctx: discord.ext.commands.Context) -> discord.Embed:
        """
        Builds the message for eggs
        """
        try:
            user_id = get_ctx_user_id(ctx)
            self._is_existing_user(user_id)
            egg_count = self.trainer_service.get_egg_count(user_id)
            egg_manaphy_count = \
                self.trainer_service.get_egg_manaphy_count(user_id)
            em = discord.Embed(title="Egg Count", colour=0xD2B48C)
            em.add_field(name="Regular Egg Count", value=egg_count)
            em.add_field(name="Manaphy Egg Count", value=egg_manaphy_count)
            em.add_field(
                name="Total Egg Count",
                value=egg_count+egg_manaphy_count
            )
            return em
        except UnregisteredTrainerException:
            raise
        except Exception as e:
            msg = "Error has occurred in building egg message."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    async def hatch_egg(
        self,
        ctx: discord.ext.commands.Context,
        special_egg: str,
    ) -> None:
        """
        Generates a random battlefly from the egg
        """
        try:
            egg_count = 0
            user_id = get_ctx_user_id(ctx)
            self._is_existing_user(user_id)
            if special_egg == 'm':
                egg_count = self.trainer_service.get_egg_manaphy_count(user_id)
                if not egg_count:
                    raise NoEggCountException("manaphy")
                pkmn = self.generator.generate_battlefly("manaphy", is_egg=True)
            else:
                egg_count = self.trainer_service.get_egg_count(user_id)
                if not egg_count:
                    raise NoEggCountException("regular")
                pkmn = self.generator.generate_random_battlefly(is_egg=True)
            self.trainer_service.decrement_egg_count(user_id, special_egg)
            self.trainer_service.give_battlefly_to_trainer(
                user_id,
                pkmn,
            )
            self.status.increase_total_pkmn_count(1)
            await self.status.display_total_battlefly_caught()
            await self._post_battlefly_catch(ctx,
                                           pkmn,
                                           "hatched",
                                           None)
            self.trainer_service.save_all_trainer_data()
        except NoEggCountException:
            raise
        except UnregisteredTrainerException:
            raise
        except Exception as e:
            msg = "Error has occurred in hatching egg."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    async def exchange_battlefly(
        self,
        ctx: discord.ext.commands.Context,
        *args: str
    ) -> discord.Embed:
        """
        Exchanges five battlefly for a random battlefly with an applied exchange
        shiny multiplier
        """
        try:
            if len(args) < 5:
                raise NotEnoughExchangebattleflySpecifiedException()
            elif len(args) > 5:
                raise TooManyExchangebattleflySpecifiedException()
            user_id = get_ctx_user_id(ctx)
            self._is_existing_user(user_id)
            pkmn_to_release = self._collect_battlefly_to_release(user_id, *args)
            for pkmn_name in pkmn_to_release.keys():
                await self._process_battlefly_release(
                    user_id,
                    pkmn_name,
                    pkmn_to_release[pkmn_name]
                )
            random_pkmn = self.generator.generate_random_battlefly()
            self.trainer_service.give_battlefly_to_trainer(
                user_id,
                random_pkmn,
            )
            self.status.decrease_total_pkmn_count(4)
            await self.status.display_total_battlefly_caught()
            await self._post_battlefly_catch(ctx,
                                           random_pkmn,
                                           "exchanged battlefly for",
                                           None)
            self.trainer_service.save_all_trainer_data()
        except NotEnoughExchangebattleflySpecifiedException:
            raise
        except NotEnoughExchangebattleflyQuantityException:
            raise
        except Exception as e:
            msg = "Error has occurred in exchanging battlefly."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    def _collect_battlefly_to_release(self, user_id: str, *args: str):
        """
        Collects battlefly to release in the form of a dictionary to
        accommodate for multiple quantities of a battlefly to release
        at once
        """
        try:
            battlefly_to_release = {}
            lack_of_battlefly_quantity = []
            for pkmn_name in args:
                pkmn_name_lowercase = pkmn_name.lower()
                pkmn_quantity = \
                    self.trainer_service.get_quantity_of_specified_battlefly(
                        user_id,
                        pkmn_name_lowercase
                    )
                if not pkmn_quantity:
                    lack_of_battlefly_quantity.append(pkmn_name_lowercase)
                elif pkmn_name_lowercase not in battlefly_to_release:
                    battlefly_to_release[pkmn_name_lowercase] = 1
                else:
                    battlefly_to_release[pkmn_name_lowercase] += 1
            if lack_of_battlefly_quantity:
                raise NotEnoughExchangebattleflyQuantityException(
                    lack_of_battlefly_quantity
                )
            return battlefly_to_release
        except NotEnoughExchangebattleflyQuantityException:
            raise

    async def open_lootbox(
        self,
        ctx: discord.ext.commands.Context,
        lootbox: str
    ) -> discord.Embed:
        """
        Opens a lootbox specified by the user
        """
        try:
            user_id = get_ctx_user_id(ctx)
            username = ctx.message.author.name
            self._is_existing_user(user_id)
            lootbox_quantity = \
                self.trainer_service.get_lootbox_quantity(user_id, lootbox)
            if lootbox_quantity < 1:
                raise NotEnoughLootboxQuantityException(lootbox)
            self.trainer_service.decrement_lootbox_quantity(user_id, lootbox)
            lootbox_pkmn_limit = \
                self.rates.get_lootbox_battlefly_limit()
            lootbox_pkmn_result = []
            for _ in range(lootbox_pkmn_limit):
                random_pkmn = self.generator.generate_random_battlefly(
                    lootbox=lootbox
                )
                self.trainer_service.give_battlefly_to_trainer(
                    user_id,
                    random_pkmn
                )
                random_pkmn_name = random_pkmn.name.title()
                if random_pkmn.is_shiny:
                    random_pkmn_name = "(Shiny)" + random_pkmn_name
                lootbox_pkmn_result.append(random_pkmn_name)
            self.trainer_service.save_all_trainer_data()
            self.status.increase_total_pkmn_count(lootbox_pkmn_limit)
            await self.status.display_total_battlefly_caught()
            return self._build_lootbox_results_msg(
                username,
                lootbox,
                lootbox_pkmn_result,
            )
        except NotEnoughLootboxQuantityException:
            raise
        except UnregisteredTrainerException:
            raise
        except Exception as e:
            msg = "Error has occurred in opening lootbox."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    def _build_lootbox_results_msg(
        self,
        username: str,
        lootbox: str,
        lootbox_pkmn_result: list[str],
    ) -> discord.Embed:
        """
        Builds the embedded message for the lootbox results to display in
        """
        try:
            lootbox_thumbnail = self._get_lootbox_thumbnail(lootbox)
            msg = ("**{}** opened the **{}** lootbox and obtained:\n"
                   "".format(username, lootbox.title()))
            for pkmn in lootbox_pkmn_result:
                msg += f"**{pkmn}**\n"
            em = discord.Embed(title="Lootbox",
                               description=msg,
                               colour=0xFF9900)
            em.set_thumbnail(url=lootbox_thumbnail)
            return em
        except Exception as e:
            msg = "Error has occurred in building lootbox results message"
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise

    def _get_lootbox_thumbnail(self, lootbox: str):
        """
        Determines the lootbox thumbnail based on the lootbox opened
        """
        if lootbox == self.BRONZE:
            return self.battleflyBALL_ICON_URL
        elif lootbox == self.SILVER:
            return self.GREATBALL_ICON_URL
        elif lootbox == self.GOLD:
            return self.ULTRABALL_ICON_URL

    async def display_lootbox_inventory(
        self,
        ctx: discord.ext.commands.Context
    ) -> discord.Embed:
        """
        Displays the trainer's lootbox inventory
        """
        try:
            user_id = get_ctx_user_id(ctx)
            username = ctx.message.author.name
            self._is_existing_user(user_id)
            msg = ''
            lootbox_inventory = \
                self.trainer_service.get_entire_lootbox_inventory(user_id)
            for lootbox in lootbox_inventory:
                msg += (f"**{lootbox.title()}:**"
                        f" **{lootbox_inventory[lootbox]}**\n")
            return discord.Embed(
                title="{}'s Lootboxes".format(username),
                description=msg,
                colour=0xFF9900
            )
        except UnregisteredTrainerException:
            raise
        except Exception as e:
            msg = "Error has occurred in displaying lootbox inventory"
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)
            raise
