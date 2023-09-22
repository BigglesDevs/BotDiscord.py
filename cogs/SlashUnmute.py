import discord
from discord.ext import commands
from discord import app_commands

class Unmute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print("SlashUnmute.py - ✅")

    @app_commands.command(name="unmute", description="Unmute a user")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if muted_role is None:
            await interaction.response.send_message("There is no 'Muted' role to remove.")
            return

        if muted_role not in member.roles:
            await interaction.response.send_message(f"{member.mention} is not muted.")
            return

        # Remove the muted role from the member
        await member.remove_roles(muted_role)

        # Create an embed response
        unmute_embed = discord.Embed(
            title="User Unmuted",
            color=discord.Color.green()
        )
        unmute_embed.add_field(name="User", value=member.mention, inline=False)
        unmute_embed.add_field(name="Unmuted by", value=interaction.user.mention, inline=False)

        await interaction.response.send_message(embed=unmute_embed)

# This function is required to set up the cog for use
# It will be called when you load the cog in your main bot file
async def setup(client):
    await client.add_cog(Unmute(client))
