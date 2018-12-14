def check_user_field(mongo_query, user, field):
    try:
        mongo_query["creator"][field] = user[field]
    except KeyError:
        raise ('The creator does not have %s, please check it' % field)
