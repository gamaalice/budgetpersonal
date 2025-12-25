# charts.py — charts for Version 2.0
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def embed_figure_tk(fig, frame):
    """
    Embeds a Matplotlib figure into a Tkinter frame.
    """
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.pack(fill="both", expand=True)


def chart_category_distribution(df_summary):
    """
    Pie chart of percentage by Category.
    df_summary must have columns: Category, TotalAmount.
    """
    if df_summary.empty:
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        ax.axis("off")
        return fig

    labels = df_summary["Category"].tolist()
    sizes = df_summary["TotalAmount"].tolist()

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title("Spending by category")
    return fig


def chart_category_bars(df_summary):
    """
    Bar chart of total amount per Category.
    df_summary must have columns: Category, TotalAmount.
    """
    if df_summary.empty:
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        ax.axis("off")
        return fig

    categories = df_summary["Category"].tolist()
    amounts = df_summary["TotalAmount"].tolist()

    x = range(len(categories))

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(x, amounts)
    ax.set_xticks(list(x))
    ax.set_xticklabels(categories, rotation=30, ha="right")
    ax.set_ylabel("Amount")
    ax.set_title("Total by category")
    fig.tight_layout()
    return fig
