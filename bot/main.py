import discord
import string
import requests
import re
import os

client = discord.Client()
partial_keywords = ['good morning', 'good mornin', 'goood morning']

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

    # Server count command
    if message.content.lower().startswith('-servercount'):
        await message.channel.send("I'm in " + str(len(client.guilds)) + " servers!")
        jsonbin = os.getenv('JSONBIN_BIN_ID')
        api_key = os.getenv('JSONBIN_API_KEY')
        url = 'https://api.jsonbin.io/v3/b/' + jsonbin;
        headers = {
            'Content-Type': 'application/json',
            'X-Master-Key': api_key
        }
        data = {"serverCount": str(len(client.guilds))}

        req = requests.put(url, json=data, headers=headers)
        print(req.text)

    if (' ' not in newMessage and 'mornin' in newMessage.lower()) or any(keyword in newMessage.lower() for keyword in partial_keywords):
        await message.add_reaction(r"☕")

    # Easter
    if ('easter' in newMessage.lower()):
        await message.add_reaction(r"🐰")
        await message.add_reaction(r"🥚")

    # Christmas
    # if (any(w in newMessage.lower() for w in ['christmas', 'xmas'])):
    #    await message.add_reaction(r"🎄")

    # New Year
    # if ('happy new year' in newMessage.lower()):
    #    await message.add_reaction(r"🎉")

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    # Ignore all emojis and punctuations
    newMessage = deEmojify(after.content).translate(str.maketrans('', '', string.punctuation)).strip()

    if (' ' not in newMessage and 'mornin' in newMessage.lower()) or any(keyword in newMessage.lower() for keyword in partial_keywords):
        await after.add_reaction(r"☕")


client.run(os.getenv('MORNING_COFFEE_BOT_TOKEN'))
