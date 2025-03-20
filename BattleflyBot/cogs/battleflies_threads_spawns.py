import asyncio
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_CHANNEL_ID = os.getenv("CHANNEL_ID")  # Default spawn channel

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Storage for admin-set spawn channels
spawn_channels = []

# Battle Thread System
@bot.command(name="battle")
async def start_battle(ctx, opponent: discord.Member):
    """Creates a private thread for a battle."""
    battle_name = f"{ctx.author.display_name} vs {opponent.display_name}"
    thread = await ctx.channel.create_thread(name=battle_name, type=discord.ChannelType.public_thread)
    await thread.send(f"⚔ {ctx.author.mention} is battling {opponent.mention}! Let the fight begin!")

# Set Primary Spawn Channel
@bot.command(name="setspawn")
@commands.has_permissions(administrator=True)
async def set_spawn_channel(ctx):
    """Sets the primary channel for spawns."""
    global spawn_channels
    spawn_channels = [ctx.channel.id]
    await ctx.send(f"✅ Spawns will now only appear in {ctx.channel.mention}!")

# Add Additional Spawn Channels
@bot.command(name="addspawn")
@commands.has_permissions(administrator=True)
async def add_spawn_channel(ctx):
    """Adds the current channel to the list of spawnable locations."""
    global spawn_channels
    if ctx.channel.id not in spawn_channels:
        spawn_channels.append(ctx.channel.id)
        await ctx.send(f"✅ {ctx.channel.mention} has been added as a spawn location!")
    else:
        await ctx.send(f"⚠ {ctx.channel.mention} is already a spawn location!")

# Random Spawn System
async def random_spawn():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(420)  # 7-minute spawn interval
        
        # Pick a random channel from the allowed list
        if not spawn_channels:
            spawn_channels.append(int(DEFAULT_CHANNEL_ID))  # Fallback to default
        spawn_channel = bot.get_channel(random.choice(spawn_channels))
        
        if spawn_channel:
            # Generate a Battlefly
            rarity_weights = [50, 30, 15, 4, 1]  # Common → Legendary
            rarity_labels = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
            battlefly_rarity = random.choices(rarity_labels, weights=rarity_weights)[0]
            battlefly_names = {
                "Common": ["Laceblade Ember", "Frost Reaver", "Ironshield Pansy"],
                "Uncommon": ["Rose Reaper", "Thistle Bladecaster", "Iris Tyrant"],
                "Rare": ["Acid Striker"],
                "Epic": ["Phantom Wing", "Storm Bringer"],
                "Legendary": ["Celestial Monarch"]
            }
            battlefly_name = random.choice(battlefly_names[battlefly_rarity])

            # Announce spawn
            await spawn_channel.send(f"🦋 A **{battlefly_rarity} Battlefly** ({battlefly_name}) has appeared! Type `!net` to catch it!")
        else:
            print("⚠ No valid spawn channel found!")

# Bot Events
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    bot.loop.create_task(random_spawn())

# Run Bot
bot.run(TOKEN)
