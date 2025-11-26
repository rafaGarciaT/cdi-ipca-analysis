def calc_tabela_reg(days_invested):
    if days_invested <= 180:
        return 0.255
    elif days_invested <= 360:
        return 0.2
    elif days_invested <= 720:
        return 0.175
    else:
        return 0.15