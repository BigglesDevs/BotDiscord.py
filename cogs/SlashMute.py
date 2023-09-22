import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import asyncio

class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.json_file_path = "cogs/json/muted_roles.json"

        # Load muted roles data from the JSON file if it exists
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, "r") as f:
                self.muted_roles = json.load(f)
        else:
            self.muted_roles = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        print("SlashMute.py - ✅")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # Remove the guild ID and role ID from the JSON file when the bot is kicked from a guild
        guild_id = str(guild.id)
        if guild_id in self.muted_roles:
            del self.muted_roles[guild_id]
            with open(self.json_file_path, "w") as f:
                json.dump(self.muted_roles, f, indent=4)

    @app_commands.command(name="mute", description="Mute a user")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: int = None):
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if muted_role is None:
            # Create the "Muted" role if it doesn't exist
            muted_role = await interaction.guild.create_role(name="Muted")
            # You can modify the permissions for the muted role here if needed
            # muted_role.permissions.update(...)

        # Apply the muted role to the member
        await member.add_roles(muted_role)

        if duration:
            duration_in_minutes = duration  # Duration is specified in minutes
            await interaction.response.send_message(embed=self.create_mute_embed(member, duration_in_minutes, interaction.user))
            await asyncio.sleep(duration_in_minutes * 60)  # Convert minutes to seconds
            await member.remove_roles(muted_role)
            await interaction.followup.send(embed=self.create_unmute_embed(member, duration_in_minutes, interaction.user))
        else:
            await interaction.response.send_message(embed=self.create_mute_embed(member, None, interaction.user))

        # Log guild ID and role ID
        self.log_guild_info(interaction.guild.id, muted_role.id)

    def create_mute_embed(self, member, duration=None, requester=None):
        embed = discord.Embed(
            title="User Muted",
            color=discord.Color.red()
        )
        embed.add_field(name="User", value=member.mention, inline=False)
        if duration:
            embed.add_field(name="Duration", value=f"{duration} minutes", inline=False)
        if requester:
            embed.add_field(name="Muted by", value=requester.mention, inline=False)
        embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTn8TE2_ORiU-q1DtrUy9btR5UC1akfGqDjWg&usqp=CAU")  # Change the URL to the desired image
        return embed

    def create_unmute_embed(self, member, duration=None, unmuter=None):
        embed = discord.Embed(
            title="User Unmuted",
            color=discord.Color.green()
        )
        embed.add_field(name="User", value=member.mention, inline=False)
        if duration:
            embed.add_field(name="Muted for", value=f"{duration} minutes", inline=False)
        if unmuter:
            embed.add_field(name="Unmuted by", value=unmuter.mention, inline=False)
        embed.set_image(url="https://i.pinimg.com/736x/cd/d5/e4/cdd5e4858eac95d440512d9ea2f747a2--memes-sci-fi.jpg")  # Change the URL to the desired image
        return embed

    def log_guild_info(self, guild_id, role_id):
        self.muted_roles[str(guild_id)] = role_id
        with open(self.json_file_path, "w") as f:
            json.dump(self.muted_roles, f, indent=4)

# This function is required to set up the cog for use
# It will be called when you load the cog in your main bot file
async def setup(client):
    await client.add_cog(Mute(client))
