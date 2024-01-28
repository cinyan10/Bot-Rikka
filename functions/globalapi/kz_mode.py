
def format_kzmode(mode) -> str:
    """return kz_timer, kz_simple or kz_vanilla """
    if mode in ('k', 'kzt', 0, 'kz_timer'):
        return 'kz_timer'
    elif mode in ('s', 'skz', 1, 'kz_simple'):
        return 'kz_simple'
    else:
        return 'kz_vanilla'


if __name__ == '__main__':
    rs = format_kzmode('skz')
    print(rs)

