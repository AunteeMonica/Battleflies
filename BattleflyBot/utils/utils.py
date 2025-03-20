from discord.ext import commands
import discord
import re


def format_battlefly_name(battlefly_name: str) -> str:
    """
    Replaces underscore with a space
    """
    formatted_name = battlefly_name.replace('_', ' ')
    return formatted_name.title()


def format_cocoon_battlefly_name(battlefly_name: str) -> str:
    """
    Formats the name for Battleflies obtained from Cocoons.
    """
    return battlefly_name.title()


def get_ctx_user_id(ctx: commands.Context):
    """
    Gets context author user_id returned as string
    """
    return str(ctx.message.author.id)


def get_specific_text_channel(ctx: commands.Context, channel_name: str):
    """
    Gets 'special' channel object
    """
    return discord.utils.get(ctx.message.guild.channels, name=channel_name)


def parse_discord_mention_user_id(user_mention: str):
    """
    Parses discord user ID from mention's extra symbols
    """
    parsed_user_id = re.search(r'\d+', user_mention)
    parsed_user_id = str(parsed_user_id.group(0))
    return parsed_user_id


def sort_battleflies(battleflies, sort_by="type"):
    """
    Sorts Battleflies by the given category.
    """
    sorting_methods = {
        "type": lambda b: b.get("type", ""),
        "name": lambda b: b.get("name", "")
    }
    battleflies.sort(key=sorting_methods.get(sort_by, sorting_methods["type"]))
    return battleflies
