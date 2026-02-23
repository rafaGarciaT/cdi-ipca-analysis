import pandas
from matplotlib.ticker import FuncFormatter


def format_months(month_series: pandas.Series, year_series: pandas.Series = None) -> pandas.Series:
    """Formata uma série de meses (e opcionalmente anos) para o formato 'MMM/YY'.

    Args:
        month_series (pandas.Series): Série contendo os números dos meses (1-12).
        year_series (pandas.Series, optional): Série contendo os anos correspondentes. Se fornecida, o formato será 'MMM/YY'. Se não, apenas 'MMM'.

    Returns:
        pandas.Series: Série formatada com os meses (e anos, se fornecidos) no formato 'MMM/YY' ou 'MMM'.
    """
    months_dict = {
        1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
        7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
    }

    formatted = month_series.map(months_dict)

    if year_series is not None:
        year_short = (year_series % 100).astype(str)
        formatted = formatted + '/' + year_short

    return formatted


def format_rate(x, pos):
    return f"{x:.0f}%"


def add_line(ax, x_data, y_data, color, linestyle='solid', linewidth=2, **kwargs) -> None:
    """Adiciona uma linha a um gráfico Matplotlib com formatação personalizada."""
    ax.plot(x_data, y_data, color=color, linestyle=linestyle,
             linewidth=linewidth, **kwargs)


def setup_plot(ax, title, x_label, y_label, y_lim=None, add_grid=True, add_legend=False):
    """Configura o layout de um gráfico Matplotlib, incluindo título, rótulos, formatação de eixo e opções de grade e legenda.
    Permite personalizações adicionais depos da função ser chamada.
    Notes:
        - É necessário chamar plt.show() após essa função para exibir o gráfico.
    """
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.yaxis.set_major_formatter(FuncFormatter(format_rate))
    ax.tick_params(axis="x", rotation=45)

    if y_lim:
        ax.set_ylim(y_lim)

    if add_grid:
        ax.grid(axis="y", linestyle="--", alpha=0.4)

    if add_legend:
        ax.legend()