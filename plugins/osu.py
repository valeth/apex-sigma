from plugin import Plugin
from config import cmd_osu
from utils import create_logger
import requests
from io import BytesIO
from PIL import Image
import os
class OSU(Plugin):
    is_global = True
    log = create_logger(cmd_osu)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_osu):
            await self.client.send_typing(message.channel)
            cmd_name = 'Rule34'
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            try:
                osu_input = message.content[len(pfx) + len(cmd_osu) + 1:]
                sig_url = 'https://lemmmy.pw/osusig/sig.php?colour=pink&uname=' + osu_input
                sig = requests.get(sig_url).content
                sig_img = Image.open(BytesIO(sig))
                sig_img.save('cache/img_' + message.author.id + '.png')
                await self.client.send_file(message.channel, 'cache/img_' + message.author.id + '.png')
                os.remove('cache/img_' + message.author.id + '.png')
            except:
                await self.client.send_message(message.channel, 'Something went wrong or the user was not found.')