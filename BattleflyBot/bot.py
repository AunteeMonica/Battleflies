from bot_logger import logger
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import json
import logging
import random  # Needed for spawning Battleflies
import os  # Needed for file handling

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Load bot config
CONFIG_JSON_PATH = "bot_config.json"
with open(CONFIG_JSON_PATH) as config_file:
    config_data = json.load(config_file)


INVENTORY_FILE = "battlefly_inventory.json"

def load_inventory():
    """Loads the inventory from file. Wipes any old string-based data."""
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "w") as f:
            json.dump({}, f)  # Create empty inventory

    with open(INVENTORY_FILE, "r") as f:
        inventory = json.load(f)

    return inventory  # No more conversions, just load as is


    # Define Battlefly names per rarity for conversion
    battlefly_names = {
        "Common": ["Laceblade Ember", "Frost Reaver", "Ironshield Pansy"],
        "Uncommon": ["Rose Reaper", "Thistle Bladecaster", "Iris Tyrant"],
        "Rare": ["Acid Striker"]
    }

    # Convert old string-based inventories into dictionaries
    for user_id, battleflies in inventory.items():
        new_battleflies = []
        for battlefly in battleflies:
            if isinstance(battlefly, str):  # Convert old entries
                rarity = battlefly  # The old string is just the rarity
                battlefly_name = random.choice(battlefly_names.get(rarity, ["Unknown"]))  # Assign a name
                new_battleflies.append({"name": battlefly_name, "type": rarity})
            else:
                new_battleflies.append(battlefly)
        inventory[user_id] = new_battleflies

    return inventory
  

def save_inventory(inventory):
    """Saves the inventory to file."""
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)

# Load the existing inventory when the bot starts
battlefly_inventory = load_inventory()

active_battleflies = {}  # Stores players' found Battleflies

# Load bot config
# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


# Set up bot intents
intents = Intents.default()
intents.message_content = True  # Needed for reading messages

# Initialize bot
bot = commands.Bot(command_prefix=config_data["cmd_prefix"],
                   description="Rendition of battleflyBot",
                   intents=intents,
                   help_command=None)


# Bot startup event
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

    # Load channel ID from config
    channel_id = int(CHANNEL_ID) if CHANNEL_ID else 0

    # Get the channel
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send("Bot is online! 🚀")
        print("✅ Bot message sent successfully!")
    else:
        print(f"❌ Error: Could not find channel with ID {channel_id}. Check bot permissions.")

# Handle messages
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore bot messages
    
    await bot.process_commands(message)  # Ensure commands work


# Handle command errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        # Format cooldown time to show in seconds (rounded)
        remaining_time = round(error.retry_after, 1)
        await ctx.send(f"⏳ {ctx.author.mention}, you're on cooldown! Try again in **{remaining_time} seconds.**")
    
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ {ctx.author.mention}, please enter all required arguments.")
    
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ {ctx.author.mention}, invalid arguments provided.")
    
    else:
        await ctx.send("❌ An unknown error occurred.")
    
    # Log the error
    logging.error(f"Command Error: {error}")


# Load cogs
async def load_cogs():
    try:
        await bot.load_extension("cogs.cog_manager")
        print("✅ Loaded cogs successfully!")
    except Exception as e:
        logging.error(f"Failed to load cogs: {str(e)}")

@bot.command(name="search")
@commands.cooldown(1, 30, commands.BucketType.user)  # 30 second cooldown
async def search(ctx):
    """Players can search for Battleflies"""
    
    # 70% chance to find a Battlefly
    found_battlefly = random.choices([True, False], weights=[70, 30])[0]

    if found_battlefly:
        # Determine rarity
        rarity_weights = [50, 30, 15, 4, 1]  # Common → Legendary
        rarity_labels = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
        battlefly_rarity = random.choices(rarity_labels, weights=rarity_weights)[0]

        await ctx.send(f"🔎 {ctx.author.mention} searched and found a **{battlefly_rarity} Battlefly**! Woo hoo!! Type `!catch` to try catching it!")
        
        # Store the found Battlefly for `!catch` command (we'll handle this next)
        active_battleflies[ctx.author.id] = battlefly_rarity

    else:
        await ctx.send(f"😞 {ctx.author.mention} searched, but didn't find any Battleflies this time. Try again later!")

@bot.command(name="catch")
async def catch(ctx):
    """Players attempt to catch a Battlefly they found using !search"""
    
    # Check if player has an active Battlefly encounter
    if ctx.author.id not in active_battleflies:
        await ctx.send(f"⚠️ {ctx.author.mention}, you haven't found a Battlefly yet! Use `!search` first.")
        return
    
    # Get the rarity of the Battlefly they found
    battlefly_rarity = active_battleflies[ctx.author.id]
    
    # Define catch rates based on rarity
    catch_rates = {
        "Common": 90,
        "Uncommon": 70,
        "Rare": 50,
        "Epic": 30,
        "Legendary": 15
    }
    
    # Determine if the catch is successful
    success = random.randint(1, 100) <= catch_rates[battlefly_rarity]
    
    if success:
        # Define Battlefly names per rarity
        battlefly_names = {
            "Common": ["Laceblade Ember", "Frost Reaver", "Ironshield Pansy"],
            "Uncommon": ["Rose Reaper", "Thistle Bladecaster", "Iris Tyrant"],
            "Rare": ["Acid Striker"]
        }

        # Randomly pick a Battlefly name from the rarity group
        battlefly_name = random.choice(battlefly_names[battlefly_rarity])

        # Add to inventory as a dictionary with name and type
        user_id = str(ctx.author.id)
        if user_id not in battlefly_inventory:
            battlefly_inventory[user_id] = []
        battlefly_inventory[user_id].append({"name": battlefly_name, "type": battlefly_rarity})
        save_inventory(battlefly_inventory)  # Save to file

        await ctx.send(f"🎉 {ctx.author.mention} caught a **{battlefly_name}**! 🦋 ({battlefly_rarity})")

    else:
        await ctx.send(f"😢 {ctx.author.mention}, the **{battlefly_rarity} Battlefly** escaped! Better luck next time.")

    # Remove the active encounter
    del active_battleflies[ctx.author.id]

@bot.command(name="inv")
async def inventory(ctx):
    """Displays the player's Battlefly collection with stacked duplicates and type-based colors."""
    
    user_id = str(ctx.author.id)

    # Check if the player has any Battleflies
    if user_id not in battlefly_inventory or not battlefly_inventory[user_id]:
        await ctx.send(f"📭 {ctx.author.mention}, your inventory is empty! Go catch some Battleflies with `!search`.")
        return

    # Retrieve player's Battleflies
    battleflies = battlefly_inventory[user_id]

    # Create a dictionary to count duplicates
    battlefly_counts = {}
    for battlefly in battleflies:
        battlefly_name = battlefly["name"]
        battlefly_type = battlefly["type"].title()  # Ensure capitalization matches type_icons

        if battlefly_name in battlefly_counts:
            battlefly_counts[battlefly_name]["count"] += 1
        else:
            battlefly_counts[battlefly_name] = {
                "type": battlefly_type,
                "count": 1
            }

    # Define color-coded icons for each type (Updated with your selection)
    type_icons = {
        "Firefly": "🔥",   # Red
        "Icefly": "❄️",   # Blue
        "Leaffly": "🍃",  # Green
        "Stonefly": "🪨", # Gray
        "Stormfly": "⚡", # Purple
        "Venomfly": "☠️", # Light Green
        "Glowfly": "✨"   # Pink
    }

    # Format the inventory display
    inventory_message = f"🦋 **{ctx.author.display_name}'s Battlefly Collection:**\n"

    for battlefly_name, data in battlefly_counts.items():
        battlefly_type = data["type"]
        icon = type_icons.get(battlefly_type, "🦋")  # Default to butterfly if type not found
        print(f"🔍 Debug - Type: {battlefly_type}, Selected Icon: {icon}")  # Debugging

        inventory_message += f"- {icon} **{battlefly_name}** ({battlefly_type}) x{data['count']}\n"

    await ctx.send(inventory_message)


# Start bot
async def main():
    try:
        logger.info('Starting bot...')
        print("Starting bot...")

        await load_cogs()
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        print("\n🔴 Bot is shutting down...")
    except Exception as e:
        logging.error(f'Bot failed to run: {str(e)}')
        print(e)
    finally:
        print("✅ Cleanup complete. Exiting...")
        await bot.close()
        asyncio.get_event_loop().stop()  # Ensures the loop is properly closed


# Run bot

if __name__ == "__main__":
    loop = asyncio.new_event_loop()  # Create a fresh event loop
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())  # Runs the bot properly
    except KeyboardInterrupt:
        print("🔴 Bot process interrupted.")
    finally:
        print("✅ Cleanup complete. Closing event loop...")
        loop.stop()
        loop.close()  # Ensure the loop fully closes

