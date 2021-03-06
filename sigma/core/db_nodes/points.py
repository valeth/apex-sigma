def default_data(server, user, points, add):
    sid = str(server.id)
    total_pts = 0
    current_pts = 0
    if add:
        total_pts = points
        current_pts = points
    data = {
        'UserID': user.id,
        'Total': total_pts,
        'Current': current_pts,
        'Servers': {sid: total_pts}
    }
    return data


def point_manipulation(db, server, user, points, add):
    collection = 'PointSystem'
    sid = str(server.id)
    data = db[collection].find_one({'UserID': user.id})
    if data:
        total_pts = data['Total']
        servers = data['Servers']
        cur_pts = data['Current']
        if sid in servers:
            if add:
                srv_pts = servers[sid] + points
                total_pts += points
            else:
                srv_pts = servers[sid]
        else:
            srv_pts = points
        if add:
            cur_pts += points
        else:
            cur_pts -= points
        servers.update({sid: srv_pts})
        db[collection].update_one({'UserID': user.id},
                                  {'$set': {'Servers': servers, 'Total': total_pts, 'Current': cur_pts}})
    else:
        data = default_data(server, user, points, add)
        db[collection].insert_one(data)


def point_grabber(db, user):
    collection = 'PointSystem'
    data = db[collection].find_one({'UserID': user.id})
    if data:
        return data
    else:
        def_data = {
            'UserID': user.id,
            'Total': 0,
            'Current': 0,
            'Servers': {}
        }
        return def_data
