from pyrogram import Client, filters 
from pyromod import listen
from pytube import YouTube
from pytube.exceptions import RegexMatchError
import time,os
from moviepy.editor import *
bot = Client("trial2s3  ",
                     bot_token="1393512956:AAHgG6hGtDkBQISv7QKNCO0uxa2nq4Y-HJY",
                     api_hash="ce82c02582127129de5bf0ff2580352e",
                     api_id="1589810")



@bot.on_message(filters .private & filters.command("start"))
async def answer(bot, message):
   
   await message.reply(f"Hi {message.from_user.first_name} welcome to this bot press /commands to see the available commands")
   
   
@bot.on_message(filters.command("download"))
async def answer(bot,query,disable_web_page_preview=True):
	
    x= await bot.ask(query.from_user.id,"**send me the link of the youtube video **")
    
    
    time.sleep(2)
    
    
    link = "https://www.youtube.com/watch?v=UNZqm3dxd2w"
    
    
    await bot.send_message(query.from_user.id,x.text)
    
    
    
    
    try:
        vd = YouTube(x.text)
        video = vd.streams.filter(progressive=True ,file_extension='mp4').desc().first()
        
        
        vid = VideoFileClip(video.download())
        print(os.listdir())
        mp3 = vid.audio.write_audiofile(vd.title+".mp3")
        mp3.close()
        vid.close()
        await bot.send_audio(query.from_user.id,audio=mp3,title=vd.title,
            caption=str(vd.title),duration=int(vd.length))
    except RegexMatchError:
        await bot.send_message(query.from_user.id,'unkonwn link')


bot.run()