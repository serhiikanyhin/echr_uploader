import numpy as np
import time
import sqlite3
import matplotlib.pyplot as plt


def create_plots(df):
    draw_plots(df)


def draw_plots(df):
    draw_distribution_plot(df)


def draw_distribution_plot(df):

    # Prepare data
    plot_df = df[['application_number_year', 'application_number']]
    plot_df = plot_df.groupby(['application_number_year']).count()
    plot_df.reset_index(inplace=True)

    # Axis values
    labels = [number_to_20_cen_year(i) for i in plot_df['application_number_year'].tolist()]
    y = plot_df['application_number'].tolist()
    x = np.arange(len(labels))

    # the width of the bars
    width = 0.5

    fig, ax = plt.subplots(figsize=(16, 8))
    bar_label = ax.bar(x, y, width, label='Number of courts')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of courts')
    ax.set_xlabel('Years')
    ax.set_title('Number of ECHR courts by year')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax.bar_label(bar_label, padding=3)

    fig.tight_layout()

    timestamp = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    plt.savefig("export/Number of ECHR courts by year " + timestamp + ".png")
    plt.show()


def number_to_20_cen_year(number):
    """
    Convert "1" to "2001", "21" to "2021" etc.
    :param number: int
    :return: formatted year
    """
    year = "2000"[:len("2000")-len(str(number))] + str(number)
    return year


if __name__ == '__main__':
    run_script()
