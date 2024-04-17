from aiogram import Bot
from aiogram.types import Message
import requests
from bs4 import BeautifulSoup as BS

async def get_start(message: Message, bot: Bot):
    await message.answer("Hey, can you send me the link to the pin and I'll download it for you!")

async def parse(message: Message, bot: Bot):
    link = message.text
    await message.answer('Please wait!')
    try:
        try:
            pin_id = link.split('/')[4]
            link = link.split('&')
            invite_code = link[0].split('=')[1]
            sender = link[1][7:]
            sfo = link[2][4:]

            headers = {
                'pin_id':pin_id,
                'invite_code': invite_code,
                'sender': sender,
                'sfo': sfo,
            }

            link = f'https://ru.pinterest.com/pin/{pin_id}/sent/?invite_code={invite_code}&sender={sender}&sfo={sfo}'
        except Exception as e:
            link = link
        req = requests.get(url=link)
        soup = BS(req.text, 'html.parser')
        div = soup.find(id="S:6").find_all('script')
        div = div[1].text.split(',')
        for index in div:
            if 'contentUrl' in index:
                div = index
        total_video_link = div[13:]
        await message.answer(total_video_link)
    except Exception as e:
        await message.answer('Error, pls try again!')
