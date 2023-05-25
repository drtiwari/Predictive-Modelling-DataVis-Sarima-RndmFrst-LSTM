import pandas as pd
from datetime import datetime

import statsmodels.api as sm
import config as c

import seaborn as sns
import numpy as np

# sns.set(
#     context="paper",
#     style="white",
#     palette="deep",
#     font="sans-serif",
#     font_scale=1.2,
#     color_codes=True,
#     rc=None,
# )

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

import warnings

warnings.filterwarnings("ignore")


# Dataframe Pre-Processing
def data_pre_processing(df):
    # Reading the data
    df["Datetime"] = [datetime.strptime(x, "%d-%m-%Y %H:%M") for x in df["Datetime"]]

    # Making sure there are no duplicated data
    # If there are some duplicates we average the data during those duplicated days
    df = df.groupby("Datetime", as_index=False)["kwh"].mean()

    # Sorting the values
    df.sort_values("Datetime", inplace=True)

    # Setting index date
    df.set_index(df["Datetime"], inplace=True)

    # Dropping column Datetime
    df.drop("Datetime", axis=1, inplace=True)

    return df


def data_outlier_removal(df, hourly=True, daily=True):
    if hourly:
        # Remove outlier data
        df.drop(df[df.kwh < 0.001].index, inplace=True)
        df.drop(df[df.kwh > 1.0].index, inplace=True)

    if daily:
        # Removing data values from dataframe
        df.drop(df[df.kwh < 2].index, inplace=True)
        df.drop(df[df.kwh > 7].index, inplace=True)

    return df


# TREND PLOT
def tsa_plot(df, model_type, periods, save_fig, fig_name):
    decomposition = sm.tsa.seasonal_decompose(df, model=model_type, period=periods)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 6))
    decomposition.observed.plot(ax=ax1, title="Observed")
    decomposition.trend.plot(ax=ax2, title="Trend")
    decomposition.seasonal.plot(ax=ax3, title="Seasonality")
    decomposition.resid.plot(ax=ax4, title="Residual", style=["o"])

    # Remove labels from first 3 graphs
    ax1.get_xaxis().set_visible(False)
    ax2.get_xaxis().set_visible(False)
    ax3.get_xaxis().set_visible(False)

    # Define the date format
    date_form = DateFormatter("%m-%d")
    ax4.xaxis.set_major_formatter(date_form)
    # Ensure a major tick for each week using (interval=1)
    ax4.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax4.set(xlabel="Date")
    plt.xticks(rotation=0)

    fig.tight_layout()

    if save_fig:
        plt.show()
        fig.savefig(f"{c.loc_fig}/{fig_name}")


# SCATTER PLOT
def data_visualization(df="df", sca_tter=False, title_name="10 secs"):
    # Plot of data with specified details, data x-axis tick labels reformatted in desired way
    fig, ax = plt.subplots()

    # Add x-axis and y-axis
    if sca_tter:
        ax.scatter(df.index.values, df["kwh"], color="Slateblue", alpha=0.6)
    else:
        ax.plot(df.index.values, df["kwh"], color="Slateblue", alpha=0.6)

    # Set title and labels for axes
    ax.set(
        xlabel="Date",
        ylabel="Energy (kWh)",
        title=f"Energy consumption per {title_name}",
    )
    # xlim=["2020-01-20", "2020-04-01"])

    # Define the date format
    date_form = DateFormatter("%d/%m")
    ax.xaxis.set_major_formatter(date_form)
    # Ensure a major tick for each week using (interval=1)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

    plt.xticks(rotation=30)

    sns.despine()
    fig.show()
    fig.savefig(f"{c.loc_fig}/plot {title_name}")


# Resampling data frame by days of week average
def data_vis_weekdays(df, title_name="Daywise average"):
    # Plotting data by the dayes of week
    fig, ax = plt.subplots()

    # Add x-axis and y-axis
    ax.plot(df.index.values, df["kwh"], marker="o", color="Slateblue", alpha=0.6)

    # Set title and labels for axes
    ax.set(
        xlabel="Date", ylabel="Energy (kWh)", title="Energy consumption daywise average"
    )

    plt.xticks(rotation=30)

    sns.despine()
    plt.show()
    fig.savefig(f"{c.loc_fig}/plot {title_name}")


# Plot donught pie chart
def data_vis_donught(df, title_name="Daywise average percentage"):
    # Plot donught pie chart
    labels = df.index
    sizes = df["kwh"]

    # colors
    # colors = ['#c88691','#ad85ba','#95a1c3', '#74a18e','#b2c891','#949494','#d6d6d6']
    colors = [
        "#687995",
        "#b78f78",
        "#6c9174",
        "#a46e70",
        "#8b84a1",
        "#85796e",
        "#c4a1ba",
    ]

    # explsion
    explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)

    plt.pie(
        sizes,
        colors=colors,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.85,
        explode=explode,
    )

    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc="white")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title("Energy consumption daytype average composition")
    # ax1.axis("equal")
    plt.tight_layout()
    plt.savefig(f"{c.loc_fig}/plot {title_name}")
    plt.show()


# Grouping whole data on hourly basis
def data_vis_area_hourly(df, title_name="Daytime average"):
    hourly = df.groupby(df.index.time).mean()

    # Creating x ticks
    hourly_x_ticks = 4 * 60 * 60 * np.arange(6)

    # Plotting data by the hours
    hourly.plot(
        kind="area", xticks=hourly_x_ticks, color="Slateblue", alpha=0.2, legend=False
    )
    plt.xlabel("Day time")
    plt.ylabel("Energy (kWh)")
    plt.title("Energy consumption daily daytime average")

    sns.despine()
    plt.savefig(f"{c.loc_fig}/plot {title_name}")
    plt.show()


# Grouping whole data on weekday and weekend basis, plotting in same graph
def data_vis_weekend_weekday(df, title_name="Daytype average"):
    weekend = np.where(df.index.weekday < 5, "Weekday", "Weekend")
    days_hour = df.groupby([weekend, df.index.time]).mean()

    # Creating x ticks
    hourly_x_ticks = 4 * 60 * 60 * np.arange(6)

    # Plotting data by the hours for weekdays and weekends in same graph
    # gca stands for 'get current axis'
    ax = plt.gca()

    days_hour.loc["Weekday"].plot(
        ax=ax, xticks=hourly_x_ticks, ylim=(0, 0.5), color="skyblue"
    )
    days_hour.loc["Weekend"].plot(
        ax=ax, xticks=hourly_x_ticks, ylim=(0, 0.5), color="navy"
    )

    # Modify legend
    ax.legend(["Weekdays", "Weekend"], frameon=False)

    plt.xlabel("Day time")
    plt.ylabel("Energy (kWh)")
    plt.title("Energy consumption daytype average")

    sns.despine()
    plt.savefig(f"{c.loc_fig}/plot {title_name}")
    plt.show()
