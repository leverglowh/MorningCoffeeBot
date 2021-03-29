import discord
import os

client = discord.Client()
partial_keywords = ['good morning', 'good mornin']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if (' ' not in message.content and 'mornin' in message.content) or any(keyword in message.content.lower() for keyword in partial_keywords):
        await message.add_reaction(r"☕")


client.run(os.getenv('MORNING_COFFEE_BOT_TOKEN'))
