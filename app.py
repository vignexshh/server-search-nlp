import os
import discord
from discord.ext import commands
from discord import app_commands
import openai

# Initialize the Discord bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!", activity=discord.Game(name="Chat with AI"))

# Set your OpenAI and Discord tokens
OPENAI_API_KEY = 'your_openai_api_key_here'
DISCORD_TOKEN = 'your_discord_token_here'
GUILD_ID = 'specific_guild_id_here'  # Ensure this is a string of numbers, e.g., '123456789012345678'

openai.api_key = OPENAI_API_KEY

async def fetch_context(channel, limit=500):
    """
    Fetch a number of messages from a channel for context.
    """
    messages = await channel.history(limit=limit).flatten()
    return " ".join([message.content for message in messages if not message.author.bot])

@bot.tree.command(name="chat", description="Talk to the AI based on the channel's message history.")
@app_commands.describe(question="What would you like to ask the AI?")
async def chat(interaction: discord.Interaction, question: str):
    # Get historical messages for context
    context = await fetch_context(interaction.channel)

    # Query the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can choose an appropriate model
        prompt=f"{context} {question}",
        max_tokens=150
    )
    await interaction.response.send_message(response.choices[0].text.strip())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    for guild in bot.guilds:
        if str(guild.id) == GUILD_ID:
            tree = bot.tree
            tree.copy_global_to(guild=guild)
            await tree.sync(guild=guild)
            print(f"Commands synced to guild {guild.name}")

bot.run(DISCORD_TOKEN)
