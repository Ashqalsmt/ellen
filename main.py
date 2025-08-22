from pyrogram import Client
from pyrogram import  filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions

from asSQL import Client as cl


data = cl("protect")
db = data['data']
db.create_table()
db.set("botname",['الين' , 'إلين' , 'بوت' ,'الينا' , 'حلوه'])
db.set("bad_words",['كس','عير','طيز','زب','كسمك','كسختك','طيزك','مص'])

plugins = dict(root="plugins")

Client("x",
api_id=27110035,
api_hash="d1a8ec645702334d7526b6cfac843d8e",
bot_token="8350901633:AAHLK5xywxGdyah3JuCjHFEYhq7CYmo-Oog", plugins=plugins).run()
