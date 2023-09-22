import discord
from discord.ext import commands
import random

# Create a class for the EightBallCog, which is a cog for the magic 8-ball command
class EightBallCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Cog listener: This function is called when the cog is loaded and ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("MagicEightball.py - ✅")  # Print a message to indicate that the cog is ready

    # Command: Magic_EightBall
    @commands.command(aliases=["8ball", "eightball"])
    async def magic_eightball(self, ctx, *, question):
        # Define your eight ball responses in a list
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]

        # Get a random response from the list
        response = random.choice(responses)

        # Send the response to the channel where the command was invoked
        await ctx.send(response)

# Function to set up the EightBallCog and add it to the bot
async def setup(client):
   await client.add_cog(EightBallCog(client))
