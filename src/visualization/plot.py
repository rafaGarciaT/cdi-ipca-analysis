from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter


def format_months(month_series, year_series=None):
    months_dict = {
        1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
        7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
    }

    formatted = month_series.map(months_dict)

    if year_series is not None:
        year_short = (year_series % 100).astype(str)
        formatted = formatted + '/' + year_short

    return formatted


def format_rate(x):
    return f"{x:.0f}%"


def add_line(ax, x_data, y_data, color, linestyle='solid', linewidth=2, **kwargs):
    ax.plot(x_data, y_data, color=color, linestyle=linestyle,
             linewidth=linewidth, **kwargs)


def setup_plot(ax, title, x_label, y_label, y_lim=None, add_grid=True, add_legend=False):
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