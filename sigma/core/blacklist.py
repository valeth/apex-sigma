from config import permitted_id


def check_black(db, message):
    if message.author.id in permitted_id:
        return False

    if not message.server:
        return False

    black_channel   = False
    black_user      = False
    server_is_black = False

    channel_blacklist = db.get_settings(message.server.id, 'BlacklistedChannels') or []
    user_blacklist    = db.get_settings(message.server.id, 'BlacklistedUsers') or []

    black_user      = message.author.id in user_blacklist
    black_channel   = message.channel.id in channel_blacklist
    server_is_black = db.get_settings(message.server.id, 'IsBlacklisted')

    return (black_channel or black_user or server_is_black)
