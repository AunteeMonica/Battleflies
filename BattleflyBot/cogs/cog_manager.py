from cogs import AdminCommands, DailyCommands, InventoryCommands, MiscCommands, NightVendorCommands, battleflyBotTasks


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
    await bot.add_cog(DailyCommands(bot))
    await bot.add_cog(InventoryCommands(bot))
    await bot.add_cog(MiscCommands(bot))
    await bot.add_cog(NightVendorCommands(bot))
    await bot.add_cog(battleflyBotTasks(bot))
    print("battleflyBot online")
