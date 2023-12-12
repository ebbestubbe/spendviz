import matplotlib.pyplot as plt
import pandas as pd

import data


def plot_data(df):
    # fig, ax = plt.subplots(nrows=2)
    # ax[0].plot(df['date'], df['amount'])
    # ax[1].plot(df['date'], df['balance'])
    mosaic = """
    A
    B
    C
    """

    fig = plt.figure(layout="constrained", figsize=(15, 10))
    ax_dict = fig.subplot_mosaic(mosaic)
    ax_dict["A"].plot(df["date"], df["amount"])
    ax_dict["B"].plot(df["date"], df["balance"])
    ax_dict["C"].hist(df["amount"], bins=100)
    return fig, ax_dict


def statsmeup(df):
    print(df.describe())


def main():
    filename = "eksport_small"
    # process_data(filename=filename)

    df = data.read_clean(filename)
    statsmeup(df)
    df2 = data.attach_categories(df)
    print("foo")
    plot_data(df)
    plt.show()


if __name__ == "__main__":

    main()
