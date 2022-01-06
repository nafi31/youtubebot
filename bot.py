
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from pyromod import listen
from pytube import YouTube, Search
from pytube.exceptions import RegexMatchError
from base64 import urlsafe_b64decode, urlsafe_b64encode
import os
import requests
import time
import base64
from moviepy.editor import *

bot = Client("start ",
             bot_token="5022200001:AAEMupSxnxJ5UjViS1Vyvud87zVUQVCGgUU",
             api_hash="ce82c02582127129de5bf0ff2580352e",
             api_id="1589810")


def lock(name):
    name = urlsafe_b64encode(name.encode()).decode("ascii")
    stripped = name.strip("=")
    return stripped


def unlock(encoded):
    stripped = encoded.strip("=")

    padding = -len(stripped) % 4
    orignal_encoded = encoded + ('=' * padding)
    decoded = urlsafe_b64decode(orignal_encoded.encode()).decode("ascii")
    return decoded


@bot.on_message(filters.private & filters.command("start"))
async def answer(bot, message):

    await message.reply(f"Hi {message.from_user.first_name} welcome to YTA bot press \n /commands to see the available commands")


@bot.on_message(filters.private & filters.command("commands"))
async def reply(cls, msg):
    await msg.reply("Use \n /download to download audio with a link \n /search to search a video with a name  \n /help to report bugs")


# @bot.on_message(filters.user("@nafiyad1"))
# async def reply(cls, msg):
    # if msg.reply_to_message:
 #   print(msg)
 #   await bot.send_message(msg.reply_to_message.chat.id, msg.text)


@bot.on_message(filters.private & filters.command("help"))
async def reply(cls, msg):
    issue = await bot.ask(msg.from_user.id, "what type of issues are you facing please elaborate in a text we wont reply but we will release the patch A.S.A.P", reply_markup=ReplyKeyboardMarkup([
        ["cancel"],

    ], resize_keyboard=True))
    if issue.text != "cancel" and issue.text != "/start" and issue.text != "/help" and issue.text != "/download" and issue.text != "/search":
        print("y")
        await issue.forward(383694032)
        print("z")
        await bot.send_message(383694032, f"username @{msg.from_user.username} \n id {msg.from_user.id} \n bug issue: {issue.text}")

        await bot.send_message(msg.from_user.id, "Your response was sent , thanks for reporting ", reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(msg.from_user.id, "report cancelled", reply_markup=ReplyKeyboardRemove())


@bot.on_message(filters.private & filters.command("search"))
async def search(cls, msg):
    x = await bot.ask(msg.from_user.id, "**send me the name of the video and copy the video id from the result and send it to me**")
    vd = Search(x.text)
    res = ""
    count = 0
    for i in vd.results:
        count = count + 1
        if count <= 5:

            res = res + \
                f"{i.title} \n\n/yt_{lock(i.video_id)} \n\n "

    await bot.send_message(msg.from_user.id, res)


@bot.on_message(filters.private & filters.regex("/yt_.*"))
async def reply(bot, msg):
    try:
        print("https://youtu.be/"+unlock(msg.text.split("_")[1]))
        thmb = YouTube("/"+unlock(msg.text.split("_")[1]))
        name = thmb.title
        if not os.path.isfile(name+".jpg"):

            t = str.maketrans('/\\""', "    ")
            name = name.translate(t)

            re = requests.get(thmb.thumbnail_url)
            img = open(name+".jpg", "wb")
            img.write(re.content)
            img.close()
        else:
            pass

        await bot.send_message(msg.from_user.id, "downloading the video please wait , might take 1-2 mins because of shortage of server funds , dm  @nafiyad1 to save the bot")

        try:
            vd = YouTube("https://youtu.be/"+unlock(msg.text.split("_")[1]))
            # opens the link if its valid
            video = vd.streams.filter(
                progressive=True, file_extension='mp4').desc().first()
            # filtering the highest quality of the video available

            vid = VideoFileClip(video.download())
            # setting up the video file to be converted to mp3 in this case the youtube video the user provided with a link

            mp3 = name+".mp3"
            # sets the audio file name as the youtube videos title
            file = vid.audio.write_audiofile(mp3)
            # writting the mp3 file

            vid.close()
            await bot.send_chat_action(msg.from_user.id, "upload_audio")
            await bot.send_audio(msg.from_user.id, audio=mp3, title=name,
                                 caption=str(name)+"\n via @ytaudiosaverbot", thumb=name+".jpg", duration=int(vd.length), performer=vd.author)
        except RegexMatchError:
            # checks if the given user input is valid if not returns the ff message
            await bot.send_message(msg.from_user.id, '**Link not valid** \n please try again')
    except RegexMatchError:
        pass


@bot.on_message(filters.command("download"))
async def answer(cls, msg):
    x = await bot.ask(msg.from_user.id, "**send me the link of the youtube video **")
    # asks user for input
    await bot.send_message(msg.from_user.id, "downloading the video please wait, might take 1-2 mins because of shortage of server funds, dm  @nafiyad1 to save the bot")
    thmb = YouTube(msg.text)
    re = requests.get(thmb.thumbnail_url)
    with open(thmb.title+".jpg", "wb") as img:
        img.write(re.content)
        img.close()
    try:
        vd = YouTube(x.text)
        # opens the link if its valid
        video = vd.streams.filter(
            progressive=True, file_extension='mp4').desc().first()
        # filtering the highest quality of the video available

        vid = VideoFileClip(video.download())
        # setting up the video file to be converted to mp3 in this case the youtube video the user provided with a link

        mp3 = vd.title+".mp3"
        # sets the audio file name as the youtube videos title
        file = vid.audio.write_audiofile(mp3)
        # writting the mp3 file

        vid.close()
        await bot.send_chat_action(msg.from_user.id, "upload_audio")
        await bot.send_audio(msg.from_user.id, audio=mp3, title=vd.title,
                             caption=str(vd.title)+"\n via @ytaudiosaverbot", thumb=vd.title+".jpg", duration=int(vd.length), performer=vd.author)
    except RegexMatchError:
        # checks if the given user input is valid if not returns the ff message
        await bot.send_message(msg.from_user.id, '**Link not valid** \n please try again')


bot.run()
