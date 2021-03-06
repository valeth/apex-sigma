﻿import discord
from sigma.core.permission import check_man_msg


async def blockinvites(cmd, message, args):
    if not check_man_msg(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Requires Manage Messages Permission.', color=0xDB0000)
    else:
        active = cmd.db.get_settings(message.guild.id, 'BlockInvites')
        if active:
            cmd.db.set_settings(message.guild.id, 'BlockInvites', False)
            response = discord.Embed(color=0x66CC66, title='✅ Invite Blocking Has Been Disabled')
        else:
            cmd.db.set_settings(message.guild.id, 'BlockInvites', True)
            response = discord.Embed(color=0x66CC66, title='✅ Invite Blocking Has Been Enabled')
    await message.channel.send(None, embed=response)


