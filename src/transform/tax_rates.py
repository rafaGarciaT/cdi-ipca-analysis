

def calc_tax_reg_table(days_invested: int) -> float:
    """Calcula a alíquota do imposto de renda com base no tempo de investimento. Não utilizado atualmente."""
    if days_invested <= 180:
        return 0.255
    elif days_invested <= 360:
        return 0.2
    elif days_invested <= 720:
        return 0.175
    else:
        return 0.15
