from __future__ import print_function

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_figure(fig, base_path, formats, dpi=600):
    base_path = Path(base_path)
    base_path.parent.mkdir(parents=True, exist_ok=True)
    for extension in formats:
        fig.savefig(str(base_path) + "." + extension, dpi=dpi, bbox_inches="tight")


def horizontal_bar(df, label, value, title, output_base, formats, dpi=600, n=15):
    if df is None or df.empty:
        return False
    plot_df = df.head(n).sort_values(value, ascending=True)
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(plot_df[label], plot_df[value])
    ax.set_xlabel("Documents")
    ax.set_title(title)
    fig.tight_layout()
    save_figure(fig, output_base, formats, dpi)
    plt.close(fig)
    return True


def line_chart(df, x, y, title, output_base, formats, dpi=600, group=None):
    if df is None or df.empty:
        return False
    fig, ax = plt.subplots(figsize=(9, 5))
    if group and group in df.columns:
        for label, group_df in df.groupby(group):
            group_df = group_df.sort_values(x)
            ax.plot(group_df[x], group_df[y], marker="o", label=str(label))
        ax.legend()
    else:
        plot_df = df.sort_values(x)
        ax.plot(plot_df[x], plot_df[y], marker="o")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    save_figure(fig, output_base, formats, dpi)
    plt.close(fig)
    return True
