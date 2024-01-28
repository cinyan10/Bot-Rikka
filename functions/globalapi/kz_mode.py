
def format_kzmode(mode) -> str:
    """return kz_timer, kz_simple or kz_vanilla """
    if mode == 'k' or 'kzt' or 0 or 'kz_timer':
        return 'kz_timer'
    elif mode == 's' or 'skz' or 1 or 'kz_simple':
        return 'kz_simple'
    else:
        return 'kz_vanilla'


if __name__ == '__main__':
    rs = format_kzmode('1')
    print(rs)

