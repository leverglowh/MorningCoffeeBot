import discord
import string
import re
import os

client = discord.Client()
partial_keywords = ['good morning', 'good mornin']

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # Ignore all emojis
    newMessage = deEmojify(message.content).translate(str.maketrans('', '', string.punctuation)).strip()

    if (' ' not in newMessage and 'mornin' in newMessage.lower()) or any(keyword in newMessage.lower() for keyword in partial_keywords):
        await message.add_reaction(r"☕")

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    # Ignore all emojis and punctuations
    newMessage = deEmojify(after.content).translate(str.maketrans('', '', string.punctuation)).strip()

    if (' ' not in newMessage and 'mornin' in newMessage.lower()) or any(keyword in newMessage.lower() for keyword in partial_keywords):
        await after.add_reaction(r"☕")


client.run(os.getenv('MORNING_COFFEE_BOT_TOKEN'))
