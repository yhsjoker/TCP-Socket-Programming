import config


def pack_init(n):
    return "01" + str(n).zfill(config.N_LENGTH)


def unpack_init(msg):
    return int(msg[2:2 + config.N_LENGTH])


def pack_agree():
    return "02"


def unpack_agree(msg):
    return ""


def pack_request(data):
    return "03" + str(len(data)).zfill(config.LEN_LENGTH) + data


def unpack_request(msg):
    length = int(msg[2:2 + config.LEN_LENGTH])
    return msg[2 + config.LEN_LENGTH:2 + config.LEN_LENGTH + length]


def pack_response(data):
    return "04" + str(len(data)).zfill(config.LEN_LENGTH) + data


def unpack_response(msg):
    length = int(msg[2:2 + config.LEN_LENGTH])
    return msg[2 + config.LEN_LENGTH:2 + config.LEN_LENGTH + length]


def unpack_msg(msg):
    tp = int(msg[:2])
    if tp == 1:
        return 1, unpack_init(msg)
    elif tp == 2:
        return 2, unpack_agree(msg)
    elif tp == 3:
        return 3, unpack_request(msg)
    elif tp == 4:
        return 4, unpack_response(msg)
    else:
        return None
