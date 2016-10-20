import os
import requests
from requests.auth import HTTPBasicAuth
from lxml import html
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from config import mal_un
from config import mal_pw


async def manga(cmd, message, args):
    mal_input = ' '.join(args)

    mal_url = 'https://myanimelist.net/api/manga/search.xml?q=' + mal_input
    mal = requests.get(mal_url, auth=HTTPBasicAuth(mal_un, mal_pw))
    entries = html.fromstring(mal.content)
    n = 0
    list_text = 'List of mangas found for `' + mal_input + '`:\n```'

    if len(entries) > 1:
        for entry in entries:
            n += 1
            list_text += '\n#' + str(n) + ' ' + entry[1].text
        try:
            await cmd.reply(list_text + '\n```\nPlease type the number corresponding to the manga of your choice `(1 - ' + str(
                                len(entries)) + ')`')
        except:
            await cmd.reply('The list is way too big, please be more specific...')
            return

        choice = await cmd.bot.wait_for_message(author=message.author, channel=message.channel, timeout=20)
        try:
            ani_no = int(choice.content) - 1
        except:
            await cmd.reply('Not a number or timed out... Please start over')
            return
        if choice is None:
            return
    else:
        ani_no = 0
    try:
        await cmd.typing()
        ani_id = entries[ani_no][0].text
        name = entries[ani_no][1].text
        chapters = entries[ani_no][4].text
        volumes = entries[ani_no][5].text
        score = entries[ani_no][6].text
        air_start = entries[ani_no][9].text
        if air_start == '0000-00-00':
            air_start = '???'
        air_end = entries[ani_no][10].text
        if air_end == '0000-00-00':
            air_end = '???'
        air = air_start.replace('-', '.') + ' to ' + air_end.replace('-', '.')
        synopsis = entries[ani_no][11].text.replace('[i]', '').replace('[/i]', '').replace('<br>',
                                                                                             '').replace(
            '</br>', '').replace('<br />', '').replace('&#039;', '\'').replace('&quot;', '"').replace('&mdash;',
                                                                                                      '-')
        img = entries[ani_no][12].text
        ani_type = entries[ani_no][7].text
        status = entries[ani_no][8].text
        if len(name) > 22:
            suffix = '...'
        else:
            suffix = ''
        ani_img_raw = requests.get(img).content
        ani_img = Image.open(BytesIO(ani_img_raw))
        base = Image.open('img/ani/base.png')
        overlay = Image.open('img/ani/overlay_manga.png')
        base.paste(ani_img, (0, 0))
        base.paste(overlay, (0, 0), overlay)
        font = ImageFont.truetype("big_noodle_titling_oblique.ttf", 28)
        imgdraw = ImageDraw.Draw(base)
        imgdraw.text((4, 4), '#' + ani_id, (255, 255, 255), font=font)
        imgdraw.text((227, 16), name[:21] + suffix, (255, 255, 255), font=font)
        imgdraw.text((227, 110), 'Type: ' + ani_type, (255, 255, 255), font=font)
        imgdraw.text((227, 138), 'Status: ' + status, (255, 255, 255), font=font)
        imgdraw.text((227, 166), 'Chapters: ' + chapters + ' Volumes: ' + volumes, (255, 255, 255), font=font)
        imgdraw.text((227, 194), 'Score: ' + score, (255, 255, 255), font=font)
        imgdraw.text((227, 222), air, (255, 255, 255), font=font)
        base.save('cache/ani/anime_' + message.author.id + '.png')
        await cmd.reply_file('cache/ani/anime_' + message.author.id + '.png')
        await cmd.reply('```\n' + synopsis[:256] + '...\n```\nMore at: <https://myanimelist.net/manga/' + ani_id + '/>\n')
        os.remove('cache/ani/anime_' + message.author.id + '.png')
    except IndexError:
        await cmd.reply('Number out of range, please start over...')
    except UnboundLocalError:
        pass
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply('Not found or API dun goofed...')