import discord
from discord.ext import commands

class ServerStatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.member_channel_name = "Members:"
        self.bot_channel_name = "Bots:"

    # Cog listener: This function is called when the cog is loaded and ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("ServerStats.py - ✅")  # Print a message to indicate that the cog is ready   
    
    async def create_or_move_category(self, guild):
        # Check if the category already exists
        category = discord.utils.get(guild.categories, name="Server Stats | 📊")
        
        if not category:
            # Create the category if it doesn't exist
            category = await guild.create_category("Server Stats | 📊")
        
        # Move the category to the top of the category list
        await category.edit(position=0)
        
        return category

    @commands.command()
    async def setupserverstats(self, ctx):
        await ctx.send("Setting up server stats...")
        guild = ctx.guild  # Get the guild where the command was executed
        
        # Ensure the category is created and at the top
        category = await self.create_or_move_category(guild)
        
        member_channel = discord.utils.get(category.voice_channels, name=self.member_channel_name)
        bot_channel = discord.utils.get(category.voice_channels, name=self.bot_channel_name)
        
        member_count = sum(1 for member in guild.members if not member.bot)
        bot_count = sum(1 for member in guild.members if member.bot)
        
        if not member_channel:
            member_channel = await category.create_voice_channel(self.member_channel_name)
        if not bot_channel:
            bot_channel = await category.create_voice_channel(self.bot_channel_name)
        
        await member_channel.edit(name=f"{self.member_channel_name} {member_count}")
        await bot_channel.edit(name=f"{self.bot_channel_name} {bot_count}")

    @commands.command()
    async def serverstatsremove(self, ctx):
        guild = ctx.guild  # Get the guild where the command was executed
        category = discord.utils.get(guild.categories, name="Server Stats | 📊")
        if category:
            # Delete the voice channels first
            for voice_channel in category.voice_channels:
                await voice_channel.delete()

            # Then delete the category
            await category.delete()
            await ctx.send("Server stats category and channels have been removed.")

async def setup(bot):
    await bot.add_cog(ServerStatsCog(bot))
