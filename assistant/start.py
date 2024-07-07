# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from datetime import datetime

from pytz import timezone as tz
from telethon import Button, events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.utils import get_display_name

from pyUltroid._misc import SUDO_M, owner_and_sudos
from pyUltroid.dB.base import KeyManager
from pyUltroid.fns.helper import inline_mention
from strings import get_string

from . import *

Owner_info_msg = udB.get_key("BOT_INFO_START")
custom_info = True
if Owner_info_msg is None:
    custom_info = False
    Owner_info_msg = f"""
**Owner** - {OWNER_NAME}
**OwnerID** - `{OWNER_ID}`

**Message Forwards** - {udB.get_key("PMBOT")}

**Dante [v{ultroid_version}](https://t.me.TemanDemus_id, powered by @TeamAllbots**
"""


_settings = [
    [
        Button.inline("API Key", data="cbs_apiset"),
        Button.inline("PM Bot", data="cbs_chatbot"),
    ],
    [
        Button.inline("Alive", data="cbs_alvcstm"),
        Button.inline("PM", data="cbs_ppmset"),
    ],
    [
        Button.inline("Fitur", data="cbs_otvars"),
        Button.inline("VC Tools", data="cbs_vcb"),
    ],
    [Button.inline("kembali", data="mainmenu")],
]

_start = [
    [
        Button.inline("Langs 🌐", data="lang"),
        Button.inline("Pengaturan ⚙️", data="setter"),
    ],
    [
        Button.inline("Stats ✨", data="stat"),
        Button.inline("Gcast 📻", data="bcast"),
    ],
    [Button.inline("Waktu 🌎", data="tz")],
]


@callback("ownerinfo")
async def own(event):
    msg = Owner_info_msg.format(
        mention=event.sender.mention, me=inline_mention(ultroid_bot.me)
    )
    if custom_info:
        msg += "\n\n• Powered by **@TeamAllBots**"
    await event.edit(
        msg,
        buttons=[Button.inline("Close", data="closeit")],
        link_preview=False,
    )


@callback("closeit")
async def closet(lol):
    try:
        await lol.delete()
    except MessageDeleteForbiddenError:
        await lol.answer("MESSAGE_TOO_OLD", alert=True)

# cl user cmd 
@asst_cmd(pattern="start( (.*)|$)", forwards=False, func=lambda x: not x.is_group)
async def ultroid(event):
    args = event.pattern_match.group(1).strip()
    keym = KeyManager("BOT_USERS", cast=list)
    if not keym.contains(event.sender_id) and event.sender_id not in owner_and_sudos():
        keym.add(event.sender_id)
        kak_uiw = udB.get_key("OFF_START_LOG")
        if not kak_uiw or kak_uiw != True:
            msg = f"{inline_mention(event.sender)} `[{event.sender_id}]` started your [Assistant bot](@{asst.me.username})."
            buttons = [[Button.inline("Info", "itkkstyo")]]
            if event.sender.username:
                buttons[0].append(
                    Button.mention(
                        "User", await event.client.get_input_entity(event.sender_id)
                    )
                )
            await event.client.send_message(
                udB.get_key("LOG_CHANNEL"), msg, buttons=buttons
            )
    if event.sender_id not in SUDO_M.fullsudos:
        ok = ""
        me = inline_mention(ultroid_bot.me)
        mention = inline_mention(event.sender)
        if args and args != "set":
            await get_stored_file(event, args)
        if not udB.get_key("STARTMSG"):
            if udB.get_key("PMBOT"):
                ok = "Lu hubungin bos gua pake bot ini!!!!\n\nKirim pesan lu, nanti gua infoin ke bos gua!" 
            await event.reply(
                f"Hey there {mention}, Ini Gua Asisten Bot PyDante {me}!\n\n{ok}",
                file=udB.get_key("STARTMEDIA"),
                buttons=[Button.inline("Info.", data="ownerinfo")]
                if Owner_info_msg
                else None,
            )
        else:
            await event.reply(
                udB.get_key("STARTMSG").format(me=me, mention=mention),
                file=udB.get_key("STARTMEDIA"),
                buttons=[Button.inline("Info.", data="ownerinfo")]
                if Owner_info_msg
                else None,
            )
    else:
        name = get_display_name(event.sender)
        if args == "set":
            await event.reply(
                "Choose from the below options -",
                buttons=_settings,
            )
        elif args:
            await get_stored_file(event, args)
        else:
            await event.reply(
                get_string("ast_3").format(name),
                buttons=_start,
            )


@callback("itkkstyo", owner=True)
async def ekekdhdb(e):
    text = f"Ada pengunjung baru cek Asisten Bot lu nih. Lu dapat pesan infonya pesan di log ini!\n\nNonaktifkan : {HNDLR}setdb OFF_START_LOG True"
    await e.answer(text, alert=True)


@callback("mainmenu", owner=True, func=lambda x: not x.is_group)
async def ultroid(event):
    await event.edit(
        get_string("ast_3").format(OWNER_NAME),
        buttons=_start,
    )


@callback("stat", owner=True)
async def botstat(event):
    ok = len(udB.get_key("BOT_USERS") or [])
    msg = """PyDante Asisten - Stats
Total Users - {}""".format(
        ok,
    )
    await event.answer(msg, cache_time=0, alert=True)


@callback("bcast", owner=True)
async def bdcast(event):
    keym = KeyManager("BOT_USERS", cast=list)
    total = keym.count()
    await event.edit(f"• Broadcast to {total} users.")
    async with event.client.conversation(OWNER_ID) as conv:
        await conv.send_message(
            "Masukkin pesan gikes dulu bloggg!\nUse /Batalin gikesan lu nih!!",
        )
        response = await conv.get_response()
        if response.message == "/cancel":
            return await conv.send_message("Cancelled!!")
        success = 0
        fail = 0
        await conv.send_message(f"Mulai kirim gikesan lu ke {total} users...")
        start = datetime.now()
        for i in keym.get():
            try:
                await asst.send_message(int(i), response)
                success += 1
            except BaseException:
                fail += 1
        end = datetime.now()
        time_taken = (end - start).seconds
        await conv.send_message(
            f"""
**Gikesan lu udah selesai {time_taken} seconds.**
Total Pengguna di Bot - {total}
**Dikirim ke** : `{success} users.`
**Gagal ke** : `{fail} user(s).`""",
        )


@callback("setter", owner=True)
async def setting(event):
    await event.edit(
        "Choose from the below options -",
        buttons=_settings,
    )


@callback("tz", owner=True)
async def timezone_(event):
    await event.delete()
    pru = event.sender_id
    var = "TIMEZONE"
    name = "Timezone"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "Send Your TimeZone From This List [Check From Here](http://www.timezoneconverter.com/cgi-bin/findzone.tzc)"
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelled!!",
                buttons=get_back_button("mainmenu"),
            )
        try:
            tz(themssg)
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} changed to {themssg}\n",
                buttons=get_back_button("mainmenu"),
            )
        except BaseException:
            await conv.send_message(
                "Wrong TimeZone, Try again",
                buttons=get_back_button("mainmenu"),
            )
