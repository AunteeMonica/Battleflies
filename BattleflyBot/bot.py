import os
import json
import random
import asyncio
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

# ------------------------------------------------------
# Load environment
# ------------------------------------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_CHANNEL_ID = os.getenv("CHANNEL_ID")  # Fallback if no channels are set

# ------------------------------------------------------
# Config & Inventory
# ------------------------------------------------------
CONFIG_JSON_PATH = "bot_config.json"
INVENTORY_FILE = "battlefly_inventory.json"

with open(CONFIG_JSON_PATH) as f:
    config_data = json.load(f)

def load_inventory():
    """Loads the inventory from file."""
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "w") as f:
            json.dump({}, f)
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)

def save_inventory(inventory):
    """Saves the inventory to file."""
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)

battlefly_inventory = load_inventory()

# ------------------------------------------------------
# Bot Setup
# ------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix=config_data["cmd_prefix"],
    description="BattleflyBot - Catch & Train Battleflies",
    intents=intents,
    help_command=None
)

# ------------------------------------------------------
# Channel Management for Random Spawns
# ------------------------------------------------------
# 'primary_channel_id' -> if set, all random spawns go there
# 'allowed_channels'   -> if multiple channels are allowed for random spawns
spawn_config = {
    "primary_channel_id": None,
    "allowed_channels": []
}

# ------------------------------------------------------
# Active Spawn Tracking
# ------------------------------------------------------
# 1) Server-wide random spawn: stored in 'active_spawn'
# 2) Per-user personal spawn from !search: stored in 'active_battleflies[user_id]'
active_spawn = None  # Example: {"rarity": "Common", "name": "...", "channel_id": 12345, "caught": False}
active_battleflies = {}  # Example: {user_id: "Rare", ...} to track personal spawns

# ------------------------------------------------------
# Commands
# ------------------------------------------------------
@bot.command(name="setspawnchannel", aliases=["setspawn"])
@commands.has_permissions(administrator=True)
async def set_spawn_channel(ctx):
    """
    Sets a single primary channel for all random spawns.
    Usage: !setspawnchannel (run this in the desired channel)
    """
    spawn_config["primary_channel_id"] = ctx.channel.id
    await ctx.send(f"✅ All random spawns will now appear **only** in {ctx.channel.mention}.")

@bot.command(name="addspawnchannel", aliases=["addspawn"])
@commands.has_permissions(administrator=True)
async def add_spawn_channel(ctx):
    """
    Adds the current channel to the random spawn list (rotation or random pick).
    Usage: !addspawnchannel (run this in the desired channel)
    """
    channel_id = ctx.channel.id
    if channel_id not in spawn_config["allowed_channels"]:
        spawn_config["allowed_channels"].append(channel_id)
        await ctx.send(f"✅ {ctx.channel.mention} added to **random spawn** list.")
    else:
        await ctx.send(f"⚠️ {ctx.channel.mention} is already in the spawn list.")

@bot.command(name="removespawnchannel", aliases=["removespawn"])
@commands.has_permissions(administrator=True)
async def remove_spawn_channel(ctx, channel: discord.TextChannel = None):
    """
    Removes a channel from the random spawn list.
    
    Usage:
      1) !removespawn         (run in the channel you want to remove)
      2) !removespawn #some-channel
    """
    # If no channel is mentioned, default to the current channel
    if channel is None:
        channel_id = ctx.channel.id
    else:
        channel_id = channel.id

    if channel_id in spawn_config["allowed_channels"]:
        spawn_config["allowed_channels"].remove(channel_id)
        await ctx.send(f"✅ Removed <#{channel_id}> from the spawn list.")
    else:
        await ctx.send(f"⚠️ <#{channel_id}> is not in the spawn list.")

@bot.command(name="inventory")
async def inventory(ctx):
    """
    Sends the user's Battlefly inventory via DM.
    """
    user_id_str = str(ctx.author.id)
    user_inv = battlefly_inventory.get(user_id_str, [])
    if not user_inv:
        inv_msg = "Your inventory is empty."
    else:
        inv_msg = "Your Battleflies:\n"
        for idx, bf in enumerate(user_inv, start=1):
            inv_msg += f"{idx}. {bf['name']} ({bf['type']})\n"

    try:
        await ctx.author.send(inv_msg)
        await ctx.send(f"✉️ {ctx.author.mention}, check your DMs for your inventory!")
    except discord.Forbidden:
        await ctx.send(f"⚠️ {ctx.author.mention}, I can't DM you. Please enable DMs!")

@bot.command(name="battle")
async def battle(ctx, opponent: discord.Member):
    """
    Starts a battle in a dedicated thread to reduce spam in the main channel.
    Example usage: !battle @SomeUser
    """
    if opponent == ctx.author:
        await ctx.send("You can't battle yourself!")
        return

    thread = await ctx.channel.create_thread(
        name=f"{ctx.author.name} vs {opponent.name}",
        type=discord.ChannelType.public_thread
    )
    await thread.send(f"{ctx.author.mention} challenged {opponent.mention} to a battle here!")
    # Actual battle logic would go here (turns, damage, etc.).

# ------------------------------------------------------
# SEARCH Command (Personal Spawns)
# ------------------------------------------------------
@bot.command(name="search")
@commands.cooldown(1, 120, commands.BucketType.user)  # 2-minute cooldown
async def search(ctx):
    """Players can search for a personal Battlefly to catch."""
    # Example event check
    wild_swarm_active = False  # TODO: implement event checks if needed
    search_success_rate = 0.6 if not wild_swarm_active else 0.9

    # Determine if user finds a Battlefly
    found_battlefly = random.choices(
        [True, False],
        weights=[search_success_rate * 100, (1 - search_success_rate) * 100]
    )[0]

    if found_battlefly:
        rarity_weights = [50, 30, 15, 4, 1]  # Common → Legendary
        rarity_labels = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
        battlefly_rarity = random.choices(rarity_labels, weights=rarity_weights)[0]

        await ctx.send(
            f"🔎 {ctx.author.mention} searched and found a **{battlefly_rarity} Battlefly**! "
            f"Type `!net` to try catching it!"
        )

        # Store in active_battleflies for this user
        active_battleflies[ctx.author.id] = battlefly_rarity
    else:
        await ctx.send(
            f"😞 {ctx.author.mention} searched but didn't find any Battleflies this time. Try again later!"
        )

# ------------------------------------------------------
# NET Command (Captures Either Personal or Random Spawn)
# ------------------------------------------------------
@bot.command(name="net")
async def net(ctx):
    """
    Attempt to catch either:
      1) The user's personal spawn from !search, if it exists, OR
      2) The active random spawn in the channel, if any and not caught.
    """
    global active_spawn

    # 1) Check if user has a personal spawn from !search
    if ctx.author.id in active_battleflies:
        # They have a personal Battlefly
        battlefly_rarity = active_battleflies[ctx.author.id]

        # Define net success rates for personal spawns
        net_rates = {
            "Common": 90,
            "Uncommon": 70,
            "Rare": 50,
            "Epic": 30,
            "Legendary": 15
        }
        success_chance = net_rates.get(battlefly_rarity, 50)
        success = (random.randint(1, 100) <= success_chance)

        if success:
            # Example name sets (re-used from random spawns)
            battlefly_names = {
                "Common": ["Laceblade Ember", "Frost Reaver", "Ironshield Pansy"],
                "Uncommon": ["Rose Reaper", "Thistle Bladecaster", "Iris Tyrant"],
                "Rare": ["Acid Striker"],
                "Epic": ["Glimmer Knight"],
                "Legendary": ["Aurora Prime"]
            }
            chosen_name = random.choice(battlefly_names[battlefly_rarity])

            user_id_str = str(ctx.author.id)
            if user_id_str not in battlefly_inventory:
                battlefly_inventory[user_id_str] = []
            battlefly_inventory[user_id_str].append({
                "name": chosen_name,
                "type": battlefly_rarity
            })
            save_inventory(battlefly_inventory)

            await ctx.send(
                f"🎉 {ctx.author.mention} netted a **{chosen_name}**! 🦋 ({battlefly_rarity})"
            )
        else:
            await ctx.send(
                f"😢 {ctx.author.mention}, the **{battlefly_rarity} Battlefly** escaped! Better luck next time."
            )

        # Remove the personal spawn entry
        del active_battleflies[ctx.author.id]
        return

    # 2) If no personal spawn, check for a random spawn in this channel
    if active_spawn and not active_spawn["caught"]:
        if ctx.channel.id != active_spawn["channel_id"]:
            await ctx.send("⚠️ There's no Battlefly here for you to net!")
            return

        # Mark it caught
        active_spawn["caught"] = True
        user_id_str = str(ctx.author.id)
        if user_id_str not in battlefly_inventory:
            battlefly_inventory[user_id_str] = []
        battlefly_inventory[user_id_str].append({
            "name": active_spawn["name"],
            "type": active_spawn["rarity"]
        })
        save_inventory(battlefly_inventory)
        await ctx.send(
            f"🎉 {ctx.author.mention} caught a **{active_spawn['name']}**!"
        )
    else:
        # No personal spawn for the user, and no random spawn in this channel
        await ctx.send("😞 No wild Battlefly is currently available to net!")

# ------------------------------------------------------
# Background Random Spawning
# ------------------------------------------------------
async def random_spawn_loop():
    """
    Continuously spawns a random Battlefly at intervals.
    """
    global active_spawn
    while True:
        try:
            await asyncio.sleep(7 * 60)  # 7-minute interval
        except asyncio.CancelledError:
            # Exit cleanly if shutdown
            return

        # Spawn only if none is active or the existing one was caught
        if active_spawn is None or active_spawn.get("caught", True):
            # Pick the channel
            if spawn_config["primary_channel_id"]:
                target_channel = bot.get_channel(spawn_config["primary_channel_id"])
            else:
                candidate_ids = spawn_config["allowed_channels"]
                if not candidate_ids:
                    # Fallback to default .env channel
                    candidate_ids = [int(DEFAULT_CHANNEL_ID)]
                rand_id = random.choice(candidate_ids)
                target_channel = bot.get_channel(rand_id)

            if not target_channel:
                # If no valid channel found, skip
                continue

            # Determine rarity
            rarity_weights = [50, 30, 15, 4, 1]
            rarity_labels = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
            chosen_rarity = random.choices(rarity_labels, weights=rarity_weights)[0]

            # Name selection
            battlefly_names = {
                "Common": ["Laceblade Ember", "Frost Reaver", "Ironshield Pansy"],
                "Uncommon": ["Rose Reaper", "Thistle Bladecaster", "Iris Tyrant"],
                "Rare": ["Acid Striker"],
                "Epic": ["Glimmer Knight"],
                "Legendary": ["Aurora Prime"]
            }
            chosen_name = random.choice(battlefly_names[chosen_rarity])

            # Create active_spawn
            active_spawn = {
                "rarity": chosen_rarity,
                "name": chosen_name,
                "channel_id": target_channel.id,
                "caught": False
            }

            # Announce in channel (rarity shown, name hidden for the spawn message)
            await target_channel.send(
                f"🦋 A **{chosen_rarity} Battlefly** has appeared! "
                f"Type `!net` to catch it – first come, first serve!"
            )

# ------------------------------------------------------
# New Commands: Clear Primary Spawn & List All Spawns
# ------------------------------------------------------
@bot.command(name="clearspawn")
@commands.has_permissions(administrator=True)
async def clear_spawn_channel(ctx):
    """
    Clears the primary spawn channel, allowing spawns in multiple channels again.
    Usage: !clearspawn
    """
    if spawn_config["primary_channel_id"]:
        spawn_config["primary_channel_id"] = None
        await ctx.send("✅ Primary spawn channel cleared. The bot will now use allowed spawn channels.")
    else:
        await ctx.send("⚠️ No primary spawn channel is currently set.")

@bot.command(name="listspawns")
@commands.has_permissions(administrator=True)
async def list_spawn_channels(ctx):
    """
    Lists the current primary spawn channel and the allowed spawn channels.
    Usage: !listspawns
    """
    primary = spawn_config["primary_channel_id"]
    allowed = spawn_config["allowed_channels"]

    if not primary and not allowed:
        await ctx.send("⚠️ No spawn channels have been set.")
        return

    msg = "**Spawn Channel Settings:**\n"
    if primary:
        msg += f"• **Primary Channel**: <#{primary}>\n"
    if allowed:
        msg += "• **Allowed Channels**:\n"
        for ch_id in allowed:
            msg += f"  - <#{ch_id}>\n"

    await ctx.send(msg)

# ------------------------------------------------------
# Event Handlers & Graceful Shutdown
# ------------------------------------------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    bot.loop.create_task(random_spawn_loop())

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = round(error.retry_after, 1)
        await ctx.send(
            f"⏳ {ctx.author.mention}, you're on cooldown! Try again in **{remaining_time} seconds.**"
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ {ctx.author.mention}, please provide all required arguments.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ {ctx.author.mention}, invalid arguments provided.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to do that.")
    else:
        await ctx.send("❌ An unknown error occurred.")
    logging.error(f"Command Error: {error}")

async def main():
    try:
        print("Starting bot...")
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        print("\n🔴 Bot is shutting down gracefully...")

        # Cancel the random spawn loop explicitly
        spawn_task = None
        for task in asyncio.all_tasks():
            if task.get_coro() and task.get_coro().__name__ == "random_spawn_loop":
                task.cancel()
                spawn_task = task

        # Wait for the random spawn loop to cleanly exit
        if spawn_task:
            try:
                await spawn_task
            except asyncio.CancelledError:
                pass  # Expected, since we're canceling it

        await asyncio.sleep(0.1)  # Small delay to let tasks exit cleanly
        await bot.close()

    finally:
        print("✅ Cleanup complete. Closing event loop...")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("🔴 Bot process interrupted.")
    finally:
        print("✅ Cleanup complete. Closing event loop...")
        loop.stop()
        loop.close()
