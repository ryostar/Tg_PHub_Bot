# Disclaimer:
#   This Repo is just an working case of ARQ API with Pyrogram.
#   Telegram May ban your bot or your account since Porns aren't allowed in Telegram.
#   We aren't reponsible for Your causes....Use with caution...
#   We recommend you to use Alt account.
#   For support https://t.me/PatheticProgrammers

import os
from aiohttp import ClientSession
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from Python_ARQ import ARQ 
from asyncio import get_running_loop
from wget import download

# Config Check-----------------------------------------------------------------
if os.path.exists("config.py"):
    from config import *
elif os.path.exists("sample_config.py"):
    from sample_config import *
else:
    raise Exception("Your Config File Is Invalid or Maybe Doesn't Exist! Please Check Your Config File or Try Again.")

# ARQ API and Bot Initialize---------------------------------------------------
session = ClientSession()
arq = ARQ("https://thearq.tech", ARQ_API_KEY, session)
pornhub = arq.pornhub
phdl = arq.phdl

app = Client("Tg_PHub_Bot", bot_token=Bot_token, api_id=6419112,
             api_hash="65fb13bc3b17d9124933b8d7f2a77cbc")
print("\nBot Started!...\n")

db = {}

async def download_url(url: str):
    loop = get_running_loop()
    file = await loop.run_in_executor(None, download, url)
    return file

async def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
    )
# Start  -----------------------------------------------------------------------
@app.on_message(
    filters.command("start") & ~filters.edited
)
async def start(_, message):
    m= await message.reply_text(
        text = "Tôi có thể giúp bạn tải về video ở PornHub"
       )

# Help-------------------------------------------------------------------------
@app.on_message(
    filters.command("help") & ~filters.edited
)
async def help(_, message):
    await message.reply_text(
        """**Dưới đây là các lệnh của tôi...**
/help : Xem hướng dẫn
/admin : Xem nhà phát triển

To Search in PHub just simply Type something"""
    )
    
# Repo  -----------------------------------------------------------------------
@app.on_message(
    filters.command("admin") & ~filters.edited
)
async def repo(_, message):
    m= await message.reply_text(
        text="""Bot này thuộc quyền sở hữu của [Kuri](https://t.me/cunongdan)""",
        disable_web_page_preview=True
       )

# Let's Go----------------------------------------------------------------------
@app.on_message(
    filters.private & ~filters.edited & ~filters.command("help") & ~filters.command("start") & ~filters.command("repo")
    )
async def sarch(_,message):
    try:
        if "/" in message.text.split(None,1)[0]:
            await message.reply_text(
                "**Usage:**\nChỉ cần nhập Một cái gì đó để tìm kiếm trong Pornhub Trực tiếp"
            )
            return
    except:
        pass
    m = await message.reply_text("Nhận kết quả.....")
    search = message.text
    try:
        resp = await pornhub(search,thumbsize="large")
        res = resp.result
    except:
        await m.edit("Không tìm thấy gì ... Hãy thử lại")
        return
    if not resp.ok:
        await m.edit("Không tìm thấy gì ... Hãy thử lại")
        return
    resolt = f"""
**Tên:** {res[0].title}
**Lượt xem:** {res[0].views}
**Đánh giá:** {res[0].rating}"""
    await m.delete()
    m = await message.reply_photo(
        photo=res[0].thumbnails[0].src,
        caption=resolt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Xem video khác",
                                         callback_data="next"),
                    InlineKeyboardButton("Xóa",
                                         callback_data="delete"),
                ],
                [
                    InlineKeyboardButton("Tải về",
                                         callback_data="dload")
                ]
            ]
        ),
        parse_mode="markdown",
    )
    new_db={"result":res,"curr_page":0}
    db[message.chat.id] = new_db
    
 # Next Button--------------------------------------------------------------------------
@app.on_callback_query(filters.regex("next"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("Có lỗi xảy ra ..... **Tìm kiếm lại**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page+1
    db[query.message.chat.id]['curr_page'] = cur_page
    if len(res) <= (cur_page+1):
        cbb = [
                [
                    InlineKeyboardButton("Video trước",
                                         callback_data="previous"),
                    InlineKeyboardButton("Tải về",
                                         callback_data="dload"),
                ],
                [
                    InlineKeyboardButton("Xóa",
                                         callback_data="delete"),
                ]
              ]
    else:
        cbb = [
                [
                    InlineKeyboardButton("Trước",
                                         callback_data="previous"),
                    InlineKeyboardButton("Sau",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("Xóa",
                                         callback_data="delete"),
                    InlineKeyboardButton("Tải",
                                         callback_data="dload")
                ]
              ]
    resolt = f"""
**Tên:** {res[cur_page].title}
**Lượt xem:** {res[cur_page].views}
**Đánh giá:** {res[cur_page].rating}"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )
 
# Previous Button-------------------------------------------------------------------------- 
@app.on_callback_query(filters.regex("previous"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("Xãy ra lỗi ..... **Search Again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1
    db[query.message.chat.id]['curr_page'] = cur_page
    if cur_page != 0:
        cbb=[
                [
                    InlineKeyboardButton("Lùi lại",
                                         callback_data="previous"),
                    InlineKeyboardButton("Tiếp theo",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("Xóa",
                                         callback_data="delete"),
                    InlineKeyboardButton("Tải",
                                         callback_data="dload")
                ]
            ]
    else:
        cbb=[
                [
                    InlineKeyboardButton("Tiếp",
                                         callback_data="next"),
                    InlineKeyboardButton("Xóa",
                                         callback_data="Delete"),
                ],
                [
                    InlineKeyboardButton("Tải",
                                         callback_data="dload")
                ]
            ]
    resolt = f"""
**Tên:** {res[cur_page].title}
**Lượt xem:** {res[cur_page].views}
**Đánh xóa:** {res[cur_page].rating}"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )

# Download Button--------------------------------------------------------------------------    
@app.on_callback_query(filters.regex("dload"))
async def callback_query_next(_, query):
    m = query.message
    data = db[m.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    dl_links = await phdl(res[curr_page].url)
    db[m.chat.id]['result'] = dl_links.result.video
    db[m.chat.id]['thumb'] = res[curr_page].thumbnails[0].src
    db[m.chat.id]['dur'] = res[curr_page].duration
    resolt = f"""
**Tên:** {res[curr_page].title}
**Lượt xem:** {res[curr_page].views}
**Đánh giá:** {res[curr_page].rating}"""
    pos = 1
    cbb = []
    for resolts in dl_links.result.video:
        b= [InlineKeyboardButton(f"{resolts.quality} - {resolts.size}", callback_data=f"phubdl {pos}")]
        pos += 1
        cbb.append(b)
    cbb.append([InlineKeyboardButton("Xóa", callback_data="delete")])
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )

# Download Button 2--------------------------------------------------------------------------    
@app.on_callback_query(filters.regex(r"^phubdl"))
async def callback_query_dl(_, query):
    m = query.message
    capsion = m.caption
    entoty = m.caption_entities
    await m.edit(f"**Tải về :\n\n{capsion}")
    data = db[m.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    thomb = await download_url(data['thumb'])
    durr = await time_to_seconds(data['dur'])
    pos = int(query.data.split()[1])
    pos = pos-1
    try:
        vid = await download_url(res[pos].url)
    except Exception as e:
        print(e)
        await m.edit("Lỗi tải về")
        return
    await m.edit(f"**Tải lên bây giờ :\n\n'''{capsion}'''")
    await app.send_chat_action(m.chat.id, "upload_video")
    await m.edit_media(media=InputMediaVideo(vid,thumb=thomb, duration=durr, supports_streaming=True))
    await m.edit_caption(caption=capsion, caption_entities=entoty)
    if os.path.isfile(vid):
        os.remove(vid)
    if os.path.isfile(thomb):
        os.remove(thomb)
    
# Delete Button-------------------------------------------------------------------------- 
@app.on_callback_query(filters.regex("delete"))
async def callback_query_delete(_, query):
    await query.message.delete()
    
app.run()
