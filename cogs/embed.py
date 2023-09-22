import discord
from discord.ext import commands

class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("embed.py - ✅")

    @commands.command()
    async def create_embed(self, ctx, *, args):
        # Split the arguments by a specific character, like "|"
        args_list = args.split("|")

        # Ensure we have at least a title and color
        if len(args_list) < 2:
            await ctx.send("Please provide a title and color for the embed.")
            return

        # Extract the title and color
        title = args_list[0]
        color = args_list[-1]

        # Extract the description (everything between title and color)
        description = "|".join(args_list[1:-1])

        # Create the embed
        embed = discord.Embed(title=title, description=description, color=int(color, 16))

        # Send the embed
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Embed(client))
