from typing_extensions import final
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from pyrogram.types.messages_and_media import message
from pyromod import listen
from pytube import YouTube, Search
from pytube.exceptions import RegexMatchError

import os
import requests
import time
import base64
from moviepy.editor import *
bot = Client("start  ",
             bot_token="5022200001:AAEMupSxnxJ5UjViS1Vyvud87zVUQVCGgUU",
             api_hash="ce82c02582127129de5bf0ff2580352e",
             api_id="1589810")


@bot.on_message(filters.private & filters.command("start"))
async def answer(bot, message):

    await message.reply(f"Hi {message.from_user.first_name} welcome to this bot press \n /commands to see the available commands")


@bot.on_message(filters.private & filters.command("commands"))
async def reply(cls, msg):
    await msg.reply("Use /download to download audio with a link \n /search to search a video with a name  \n /help to report bugs")


@bot.on_message(filters.private & filters.command("help"))
async def reply(cls, msg):
    issue = await bot.ask(msg.from_user.id, "what type of issues are you facing please elaborate in a text we wont reply but we will release the patch A.S.A.P")

    await bot.send_message(383694032, f"username @{msg.from_user.username} \n id {msg.from_user.id} \n bug issue: {issue.text}")
    await bot.send_message(msg.from_user.id, "Your response was sent , thanks for reporting ")


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
                f"{i.title} \n [copy] -->`/{i.video_id}` \n\n "

    await bot.send_message(msg.from_user.id, res)


@bot.on_message(filters.private & filters.regex("..........."))
async def reply(bot, msg):
    try:
        thmb = YouTube(msg.text)
        re = requests.get(thmb.thumbnail_url)
        with open(thmb.title+".jpg", "wb") as img:
            img.write(re.content)
            img.close()
        await bot.send_message(msg.from_user.id, "downloading the video please wait might take 1-2 mins because of shortage of server funds dm to @nafiyad1 to save the bot")

        try:
            vd = YouTube(msg.text)
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
            await bot.send_audio(msg.from_user.id, audio=mp3, title=vd.title,
                                 caption=str(vd.title)+"\n via @ytaudiosaverbot", thumb=vd.title+".jpg", duration=int(vd.length), performer=vd.author)
        except RegexMatchError:
            # checks if the given user input is valid if not returns the ff message
            await bot.send_message(msg.from_user.id, '**Link not valid** \n please try again')
    except RegexMatchError:
        pass


@bot.on_message(filters.command("download"))
async def answer(cls, msg):
    x = await bot.ask(msg.from_user.id, "**send me the link of the youtube video **")
    # asks user for input
    await bot.send_message(msg.from_user.id, "downloading the video please wait might take 1-2 mins because of shortage of server funds dm to @nafiyad1 to save the bot")
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
        await bot.send_audio(msg.from_user.id, audio=mp3, title=vd.title,
                             caption=str(vd.title)+"\n via @ytaudiosaverbot", thumb=vd.title+".jpg", duration=int(vd.length), performer=vd.author)
    except RegexMatchError:
        # checks if the given user input is valid if not returns the ff message
        await bot.send_message(msg.from_user.id, '**Link not valid** \n please try again')


bot.run()
