"""Routines for plotting benchmarks."""

import csv
import mpl
import numpy as np


def plot_benchmark(
    data,
    properties,
    *,
    timeunit="seconds",
    frame=0,
    title=None,
    ylim,
    **yaxis_kwargs,
):
    """Create a plot figure.

    * `data` is a dict of label => precision_array, timing_array
    * `properties` is a dict of label => dict of arguments for `plot`
    * `frame`, if > 0, is the (one-based) index of the label after which to
      stop plotting. This allows to generate multiple frames, for a
      presentation, where one line is added in each new frame.
    * `title` is the plot title
    * `ylim` is a tuple of limits for the y axis. Should be (0, <max runtime>)

    All other keyword arguments are passed to `mpl.set_axis` for the y axis
    """

    fig_width = 14
    fig_height = 7.5
    left_margin = 1.0
    right_margin = 1.00
    top_margin = 0.5
    bottom_margin = 1.0

    w = fig_width - left_margin - right_margin
    h = fig_height - bottom_margin - top_margin

    fig = mpl.new_figure(fig_width, fig_height)
    ax = fig.add_axes(
        [
            left_margin / fig_width,
            bottom_margin / fig_height,
            w / fig_width,
            h / fig_height,
        ]
    )

    i = 0
    for label, (precision, timing) in data.items():
        i += 1
        if timeunit == "seconds":
            ax.plot(precision, timing, label=label, **properties[label])
        elif timeunit == "milliseconds":
            ax.plot(
                precision, timing * 1000.0, label=label, **properties[label]
            )
        else:
            raise ValueError(f"Invalid {timeunit=}")
        if i == frame:
            break

    ax.set_xlabel("precision (absolute error)")
    ax.set_ylabel(f"runtime ({timeunit})")
    ax.set_xscale("log")

    if title is not None:
        ax.set_title(title)

    if ylim is None:
        ylim = ax.get_ylim()
    if len(yaxis_kwargs) > 0:
        mpl.set_axis(ax, "y", ylim[0], ylim[1], **yaxis_kwargs)
    else:
        ax.set_ylim(ylim)

    ax.legend()
    ax.set_axisbelow(True)
    ax.grid(True, zorder=0, axis="y")

    return fig


def read_benchmark_series(filename, col="timing", **kwargs):
    """Read a benchmark series from the `col` of the given CSV file.

    The keyword arguments filter the CSV, e.g. `N=1000`
    """
    precisions_set = set()
    precision = []
    runtime = []
    with open(filename, encoding="utf8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            skip_row = False
            for (key, val) in kwargs.items():
                if row[key] != str(val):
                    skip_row = True
            if skip_row:
                continue  # next row
            precisions_set.add(row["precision"])
            precision.append(float(row["precision"]))
            runtime.append(float(row[col]))
    assert len(precisions_set) == len(precision)
    return np.array(precision), np.array(runtime)
