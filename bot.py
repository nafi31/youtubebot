
from http.client import BAD_REQUEST
from webbrowser import get
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from numerize import numerize
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from pyromod import listen
from pyrogram.errors import bad_request_400, FloodWait
from pytube import YouTube, Search
from pytube.exceptions import RegexMatchError
from base64 import urlsafe_b64decode, urlsafe_b64encode
import os
import re
import requests
from moviepy.editor import *
from db import getallusers, getusers, add_user

bot = Client("start ",
             bot_token=f"{os.enviro.get("BOT_T")}",
             api_hash=f"{os.enviro.get("API_HASH")}",
             api_id=f"{os.enviro.get("API_ID")}"


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
# with bot:
    # for i in getallusers():
    # print(i)
    #  order, ids = i
    #  print(ids)
    #  if ids != None:

    #     bot.send_message(ids,"Thanks for using @ytaudiosaverbot dont forget to share me")


@bot.on_message(filters.private & filters.user(383694032) & filters.command("broadcast"))
async def send(cls, msg):
    try:

        brd = await bot.ask(msg.from_user.id, "What do you want to send")
        for i in getallusers():
            order, ids = i
            if ids != None:
                await bot.send_message(ids, brd.text)
    except FloodWait as e:

        await asyncio.sleep(e.x)
    except (bad_request_400.UserIsBlocked, bad_request_400.InputUserDeactivated):
        pass


@bot.on_message(filters.private & filters.command("start"))
async def answer(bot, message):
    # print(getusers(message.from_user.id))
    if not getusers(message.from_user.id):
        add_user(message.from_user.id)
        await message.reply(f"Hi {message.from_user.first_name} welcome to YTA bot press \n /commands to see the available commands")

    else:
        # for i in getusers(message.from_user.id):
        #ord , ids = i
        # print(ids)
        await message.reply(f"Hi {message.from_user.first_name} welcome to YTA bot press \n /commands to see the available commands")


@bot.on_message(filters.private & filters.command("commands"))
async def reply(cls, msg):
    await msg.reply("\n to download a video just send me a youtube link or enter the video or artists name \n/help to report bugs")


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
    if issue.text != "cancel" and issue.text != "/start" and issue.text != "/help" and issue.text != "/download" and issue.text != "/search" and "http" not in issue.text:
        # print("y")
        await issue.forward(383694032)
        # print("z")
        await bot.send_message(383694032, f"username @{msg.from_user.username if msg.from_user.username else None} \n id {msg.from_user.id} \n bug issue: {issue.text}")

        await bot.send_message(msg.from_user.id, "Your response was sent , thanks for reporting ", reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(msg.from_user.id, "report cancelled", reply_markup=ReplyKeyboardRemove())


@bot.on_message(filters.command("totalusers") & filters.user(383694032))
async def reply(cls, msg):
    await bot.send_message(msg.from_user.id, len(getallusers()), reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Get all users", callback_data="get-users")]
    ]))
''' # users = ""
    #for i in getallusers():
      #  order , user_ids = i
      #  get_usr = await bot.get_users(user_ids)
      #  users = users + f"{get_usr.first_name} \n" 
 #   await bot.send_message(msg.from_user.id,users) '''


@bot.on_callback_query(filters.regex("get-users"))
async def reply(cls, msg):
    usr = []
    for i in getallusers():
        order, user_ids = i
        get_usr = await bot.get_users(user_ids)
        # print(type(get_usr))
        if not get_usr.first_name in usr:
            usr.append(get_usr.first_name)
    with open("name.txt", "a") as log:
        for x in usr:
            if x != "" and x != None:
                log.write(x+"\n")
        log.close()
    await bot.send_document(383694032, "name.txt")
    os.remove("name.txt")


@bot.on_message(filters.private & filters.text & ~filters.regex('/yt_.*'))
async def hmm(cls, msg):
    global next_res, res
    x = msg.text
    if not x == "/howto" and not x == "/help" and not x == "/start" and not "https://" in x:

        vd = Search(x)
        res = ""
        next_res = ""
        count = 0
        for i in vd.results:
            count = count + 1
            if count <= 3:

                res = res + \
                    f"{i.title} 👁{numerize.numerize(i.views)} \n\n/yt_{lock(i.video_id)} \n\n "
            elif count >= 3 and count <= 6:
                next_res = next_res + \
                    f"{i.title} 👁{numerize.numerize(i.views)} \n\n/yt_{lock(i.video_id)} \n\n "

        await bot.send_message(msg.from_user.id, res, reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        "next page",
                        callback_data="next-page"
                    ),
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        "How to download❔",
                        callback_data="how-to"
                    )

                ]
            ]
        ))
    elif "https://" in x:
        x = msg.text

        try:
            thmb = YouTube(x)
            re = requests.get(thmb.thumbnail_url)
            with open(thmb.title+".jpg", "wb") as img:
                img.write(re.content)
                img.close()
            try:
                vd = YouTube(x)
                # opens the link if its valid
                video = vd.streams.filter(
                    progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            # filtering the highest quality of the video available
                await bot.send_message(msg.from_user.id, "downloading the video please wait , might take 1-2 mins because of shortage of server funds , dm  @nafiyad1 to save the bot")

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


@bot.on_message(filters.private & filters.command("search"))
async def search(cls, msg):
    global next_res, res
    x = await bot.ask(msg.from_user.id, "**send me the name of the video and press the link that comes with it**")
    vd = Search(x.text)
    res = ""
    next_res = ""
    count = 0
    for i in vd.results:
        count = count + 1
        if count <= 3:

            res = res + \
                f"{i.title} 👁{numerize.numerize(i.views)} \n\n/yt_{lock(i.video_id)} \n\n "
        elif count >= 3 and count <= 6:
            next_res = next_res + \
                f"{i.title} 👁{numerize.numerize(i.views)} \n\n/yt_{lock(i.video_id)} \n\n "

    await bot.send_message(msg.from_user.id, res, reply_markup=InlineKeyboardMarkup(
        [
            [  # First row
                InlineKeyboardButton(  # Generates a callback query when pressed
                    "next page",
                    callback_data="next-page"
                ),
                InlineKeyboardButton(  # Generates a callback query when pressed
                    "How to download❔",
                    callback_data="how-to"
                )

            ]
        ]
    ))


@bot.on_message(filters.private & filters.regex("/yt_.*"))
async def reply(bot, msg):
    try:
        # print("https://youtu.be/"+unlock(msg.text.split("_")[1]))
        thmb = YouTube("/"+unlock(msg.text.split("_")[1]))
        name = thmb.title
        t = str.maketrans('/\\""', "    ")
        name = name.translate(t)
        if not os.path.isfile(name+".jpg"):

            re = requests.get(thmb.thumbnail_url)
            img = open(name+".jpg", "wb")
            img.write(re.content)
            img.close()
        else:
            pass

        try:

            vd = YouTube("https://youtu.be/"+unlock(msg.text.split("_")[1]))
            # opens the link if its valid
            video = vd.streams.filter(
                progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if video.filesize/1000000 <= 100:

                # filtering the highest quality of the video available
                await bot.send_message(msg.from_user.id, "downloading the video please wait , might take 1-2 mins because of shortage of server funds")

                vid = VideoFileClip(video.download())
                # setting up the video file to be converted to mp3 in this case the youtube video the user provided with a link

                mp3 = name+".mp3"
                # sets the audio file name as the youtube videos title
                file = vid.audio.write_audiofile(mp3)
                # writting the mp3 file

                vid.close()

                await bot.send_audio(msg.from_user.id, audio=mp3, title=name,
                                     caption=str(name)+"\n via @ytaudiosaverbot", thumb=name+".jpg", duration=int(vd.length), performer=vd.author)
            else:
                await bot.send_message(msg.from_user.id, "File is to big")
        except Exception as e:
            # checks if the given user input is valid if not returns the ff message
            await bot.send_message(msg.from_user.id, '**Link not valid** please try again')
            print(e)
    except RegexMatchError:
        pass


@bot.on_callback_query(filters.regex("next-page"))
async def reply(query, msg):
    await msg.edit_message_text(next_res, reply_markup=InlineKeyboardMarkup(
        [
            [  # First row
                InlineKeyboardButton(  # Generates a callback query when pressed
                    "first page",
                    callback_data="first-page"
                ),
                InlineKeyboardButton(  # Generates a callback query when pressed
                    "How to download❔",
                    callback_data="how-to"
                )

            ]
        ]
    ))


@bot.on_callback_query(filters.regex("first-page"))
async def reply(query, msg):
    await msg.edit_message_text(res, reply_markup=InlineKeyboardMarkup(
        [
            [  # First row
                InlineKeyboardButton(  # Generates a callback query when pressed
                    "next page",
                    callback_data="next-page"
                ),
                InlineKeyboardButton(  # Generates a callback query when pressed
                    "How to download❔",
                    callback_data="how-to"
                )

            ]
        ]
    ))


@bot.on_callback_query(filters.regex("how-to"))
async def reply(query, msg):
    await msg.answer("click on the video link you want to download its that simple", show_alert=True)


@bot.on_message(filters.regex("https://.*"))
async def answer(cls, msg):
    x = msg.text
    print(x)
    try:
        thmb = YouTube(x)
        re = requests.get(thmb.thumbnail_url)
        with open(thmb.title+".jpg", "wb") as img:
            img.write(re.content)
            img.close()
        try:
            vd = YouTube(x)
            # opens the link if its valid
            video = vd.streams.filter(
                progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if video.filesize/1000000 <= 100:
             # filtering the highest quality of the video available
                await bot.send_message(msg.from_user.id, "downloading the video please wait , might take 1-2 mins because of shortage of server funds")

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
            else:
                await bot.send_message(msg.from_user.id, "File is to big")

        except RegexMatchError:
            # checks if the given user input is valid if not returns the ff message
            await bot.send_message(msg.from_user.id, '**Link not valid** \n please try again')
    except RegexMatchError:
        pass


bot.run()
