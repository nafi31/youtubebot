from pyrogram import Client, filters 
from pyrogram.types import ReplyKeyboardMarkup
from pyromod import listen
from pytube import YouTube
from pytube.exceptions import RegexMatchError
import time,os
from moviepy.editor import *
bot = Client("start  ",
                     bot_token="5022200001:AAEMupSxnxJ5UjViS1Vyvud87zVUQVCGgUU",
                     api_hash="ce82c02582127129de5bf0ff2580352e",
                     api_id="1589810")



@bot.on_message(filters.private & filters.command("start"))
async def answer(bot, message):
   
   await message.reply(f"Hi {message.from_user.first_name} welcome to this bot press \n /commands to see the available commands")
   
@bot.on_message(filters.private &filters.command("commands"))
async def reply(cls,msg):
    await msg.reply("Use /download to download and \n /help to report bugs")
@bot.on_message(filters.private &filters.command("help"))
async def reply(cls,msg):
    issue = await bot.ask(msg.from_user.id,"what type of issues are you facing")
    bot.send_message(383694032,f"username {msg.from_user.username} \n id {msg.from_user.id} \n bug issue")
@bot.on_message(filters.command("download"))
async def answer(bot,msg):
    x= await bot.ask(msg.from_user.id,"**send me the link of the youtube video **")
    #asks user for input
    await bot.send_message(msg.from_user.id,"downloading the video please wait might take 1-2 mins because of shortage of server funds dm to @nafiyad1 to save the bot")
    
    try:
        vd = YouTube(x.text)
        #opens the link if its valid 
        video = vd.streams.filter(progressive=True ,file_extension='mp4').desc().first()
        #filtering the highest quality of the video available
        
        vid = VideoFileClip(video.download())
        #setting up the video file to be converted to mp3 in this case the youtube video the user provided with a link

        mp3 = vd.title+".mp3"
        #sets the audio file name as the youtube videos title 
        file = vid.audio.write_audiofile(mp3)
        #writting the mp3 file
        
        vid.close()
        await bot.send_audio(msg.from_user.id,audio=mp3,title=vd.title,
            caption=str(vd.title)+"via @ytaudiosaverbot",duration=int(vd.length),performer=vd.author)
    except RegexMatchError:
        #checks if the given user input is valid if not returns the ff message
        await bot.send_message(msg.from_user.id,'**Link not valid** \n please try again')


bot.run()