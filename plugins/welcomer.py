from pyrogram import Client as app, filters,enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup as mk, InlineKeyboardButton as btn
from pyrogram.types import ChatPermissions

from asSQL import Client as cl
from .is_admin import admin,add_msg,owner
data = cl("protect")
db = data['data']
@app.on_chat_member_updated()
@app.on_message(filters.new_chat_members)
def welcome(_,message):
    
    m = message.from_user.mention
    km = f"""
✨ **أهلاً وسهلاً بعضو جديد ينور مجموعتنا!** ✨

🎉 {m} **حياك الله في مجموعتنا** 🎉

╭─────── ˹🌿˼ ───────╮
│ **ɴᴀᴍᴇ** ➼ {m}
│ **ᴊᴏɪɴᴇᴅ** ➼ {message.date}
│ **ɢʀᴏᴜᴘ** ➼ {message.chat.title}
╰─────── ˹🌿˼ ───────╯

🌹 **نتمنى لك وقتاً ممتعاً معنا** 🌹
📜 **التزم بقوانين المجموعة لكي تستفيد وتفيد** 📜

⚡ **نرحب بالجميع إلا من ساء خلقه** ⚡
"""
    k = db.get(f"group_{message.chat.id}_welcome")
    if db.get(f"lock_welcome_{message.chat.id}") == False:
        if k == None:
            message.reply(km)
        else:
            kc = db.get(f"group_{message.chat.id}_welcome")
            message.reply(kc)