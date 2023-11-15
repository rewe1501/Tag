import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from config import *

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = API_ID
api_hash = API_HASH
bot_token = TOKEN
kntl = TelegramClient('kynan', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []


@kntl.on(events.NewMessage(pattern="^/start$"))
async def help(event):
  helptext = "𝘆𝗮𝗲𝗹𝗮𝗵 𝗶𝗱𝗶𝗼𝘁 𝘁𝗶𝗻𝗴𝗴𝗮𝗹 𝗸𝗲𝘁𝗶𝗸 𝗮𝗹𝗹 𝗱𝗼𝗮𝗻𝗴 𝗯𝗲𝗴𝗼 𝗯𝗮𝗻𝗴𝗲𝘁 𝗸𝗹𝗶𝗸 𝗸𝗹𝗶𝗸 𝘀𝘁𝗮𝗿𝘁 𝗺𝗮𝗸 𝗸𝗮𝗺𝘂 𝗸𝗹𝗶𝗸 𝘀𝘁𝗮𝗿𝘁,𝗸𝗮𝗹𝗼 𝗺𝗮𝘂 𝗽𝗹𝗮𝘆 𝗺𝘂𝘀𝗶𝗰 𝘁𝗶𝗻𝗴𝗴𝗮𝗹 𝗸𝗲𝘁𝗶𝗸 /𝗽𝗹𝗮𝘆 (𝗷𝘂𝗱𝘂𝗹 𝗹𝗮𝗴𝘂),𝗸𝗮𝗹𝗼 𝗺𝗮𝘂 𝗽𝗹𝗮𝘆 𝘃𝗶𝗱𝗲𝗼 𝘁𝗶𝗻𝗴𝗴𝗮𝗹 𝗸𝗲𝘁𝗶𝗸 /𝘃𝗽𝗹𝗮𝘆 (𝗷𝘂𝗱𝘂𝗹 𝘃𝗶𝗱𝗲𝗼),𝗸𝗮𝗹𝗼 𝗴𝗮 𝗻𝘆𝗮𝘂𝘁 𝗻𝗴𝗮𝗱𝘂 𝗮𝗷𝗮 𝘀𝗮𝗺𝗮 𝘀𝗲𝘀𝗲𝗽𝘂𝗵 𝘆𝗮𝗻𝗴 𝗱𝗶𝗯𝗮𝘄𝗮𝗵 𝗶𝘁𝘂."
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('𝘀𝗲𝘀𝗲𝗽𝘂𝗵', 't.me/rewe_anu'),
      ],
      [
        Button.url('𝘀𝘂𝗽𝗽𝗼𝗿𝘁', 't.me/supprotrewe'),
        Button.url('𝘁𝗵𝗶𝘀 𝗶𝘀 𝗺𝘆 𝗵𝗼𝘂𝘀𝗲', 't.me/nunagabut2'),
      ],
      [
        Button.url('𝗺𝗶𝗻𝗶𝗺𝗮𝗹 𝗻𝘆𝘂𝗺𝗯𝗮𝗻𝗴 𝗹𝗮𝗵 𝗻𝘆𝗲𝘁', 'https://link.dana.id/qr/g6f1u7du')
      ],
    )
  )
  
@kntl.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("Jangan private idiot!")
  
  is_admin = False
  try:
    partici_ = await kntl(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("luu bukan admin idiot banget bocah!")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("Minimal kasih pesan idiot banget!")
  elif event.pattern_match.group(1):
    mode = "teks"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "balas"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("Si anjeng dibilang kasih pesan mak kamu ya!")
  else:
    return await event.respond("Si anjeng dibilang kasih pesan mak kamu ya!")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in kntl.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"🐳 [{usr.first_name}](tg://user?id={usr.id})\n"
    if usrnum == 5:
      if mode == "teks":
        txt = f"{usrtxt}\n\n{msg}"
        await kntl.send_message(chat_id, txt)
      elif mode == "balas":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@kntl.on(events.NewMessage(pattern="^/stop$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('eh muka ancur orang gada tag all')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('Iya muka ancur ni gua stop.')



print("BOT AKTIF")
kntl.run_until_disconnected()
