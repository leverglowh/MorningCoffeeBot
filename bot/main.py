import discord
import string
import requests
from datetime import datetime
import re
import os
import json

tempCountDict = {}

def get_env_data_as_dict(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            return dict(tuple(line.replace('\n', '').split('='))
                for line in f.readlines() if not line.startswith('#'))
    except OSError as e:
        return {}

envData = get_env_data_as_dict('.env')

#---------------------

def readBin(key: str) -> any:
    jsonbin = os.getenv(key) or envData.get(key)
    bin_security_key = os.getenv('JSONBIN_SECURITY_KEY') or envData.get('JSONBIN_SECURITY_KEY')
    url = 'https://json.extendsclass.com/bin/' + jsonbin;
    headers = {
        'Security-key': bin_security_key
    }
    # print(url)
    req = requests.get(url, json=None, headers=headers)
    response = json.loads(req.text)
    # print(response)
    return response

def updateBin(key: str, data: dict) -> None:
    jsonbin = os.getenv(key) or envData.get(key)
    bin_security_key = os.getenv('JSONBIN_SECURITY_KEY') or envData.get('JSONBIN_SECURITY_KEY')
    url = 'https://json.extendsclass.com/bin/' + jsonbin;
    headers = {
        'Security-key': bin_security_key
    }

    req = requests.put(url, json=data, headers=headers)
    # print(req.text)

def onAddEmoji(date: str) -> None:
    global tempCountDict
    # countedDict = readBin('JSONBIN_REQUESTS_COUNT_BIN')
    todaysCount = tempCountDict.get(date, 0)
    todaysCount+=1
    tempCountDict[date] = todaysCount
    # print(date, '', todaysCount)
    # updateBin('JSONBIN_REQUESTS_COUNT_BIN', countedDict)

def parseDates(year: int) -> dict:
    dates = {}
    dates['xmasStart'] = datetime.strptime(XMAS_START_DATE, '%b %d').date().replace(year=year)
    dates['xmasEnd'] = datetime.strptime(XMAS_END_DATE, '%b %d').date().replace(year=year)
    dates['newYearStart'] = datetime.strptime(NEWYEAR_START_DATE, '%b %d').date().replace(year=year)
    dates['newYearEnd'] = datetime.strptime(NEWYEAR_END_DATE, '%b %d').date().replace(year=year+1)
    return dates

#---------------------

XMAS_START_DATE = 'Dec 1'
XMAS_END_DATE = 'Dec 31'

NEWYEAR_START_DATE = 'Dec 30'
NEWYEAR_END_DATE = 'Jan 3'

#---------------------
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
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
    global tempCountDict

    today = datetime.now()
    todayJustDate = today.strftime("%Y%m%d")
    parsedDates = parseDates(today.year)
    if message.author == client.user:
        return
    # Ignore all emojis
    newMessage = deEmojify(message.content).translate(str.maketrans('', '', string.punctuation)).strip()

    # Server count command
    if message.content.lower().startswith('-servercount'):
        await message.channel.send("I'm in " + str(len(client.guilds)) + " servers!")

        oldBinDict = readBin('JSONBIN_BIN_ID')
        # print(oldBinDict)

        oldBinDict['serverCount'] = str(len(client.guilds))

        for date in tempCountDict:
            oldBinDict['usageCount'][date] = oldBinDict['usageCount'].get(date, 0) + tempCountDict[date]

        # print(oldBinDict)
        tempCountDict = {}

        updateBin('JSONBIN_BIN_ID', oldBinDict)
        return

    if (' ' not in newMessage and 'mornin' in newMessage.lower()) or any(keyword in newMessage.lower() for keyword in partial_keywords):
        await message.add_reaction(r"☕")
        onAddEmoji(todayJustDate)

    # Easter
    if ('easter' in newMessage.lower()):
        await message.add_reaction(r"🐰")
        await message.add_reaction(r"🥚")
        onAddEmoji(todayJustDate)

    # Christmas
    if (parsedDates.get('xmasStart') <= today.date() <= parsedDates.get('xmasEnd') and any(w in newMessage.lower() for w in ['christmas', 'xmas'])):
       await message.add_reaction(r"🎄")
       onAddEmoji(todayJustDate)

    # New Year
    if (parsedDates.get('newYearStart') <= today.date() <= parsedDates.get('newYearEnd') and 'happy new year' in newMessage.lower()):
       await message.add_reaction(r"🎉")
       onAddEmoji(todayJustDate)


@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    # Ignore all emojis and punctuations
    newMessage = deEmojify(after.content).translate(str.maketrans('', '', string.punctuation)).strip()

    if (' ' not in newMessage and 'mornin' in newMessage.lower()) or any(keyword in newMessage.lower() for keyword in partial_keywords):
        await after.add_reaction(r"☕")


client.run(os.getenv('MORNING_COFFEE_BOT_TOKEN') or envData.get('MORNING_COFFEE_BOT_TOKEN'))
