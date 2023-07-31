from pathlib import Path
from benchmarkplots import read_benchmark_series, plot_benchmark

BENCHMARKS = Path("benchmarks")


def main():

    data = {
        "Fortran (gfortran)": read_benchmark_series(
            BENCHMARKS / "benchmark_sparse_cheby.csv", "QDYN_gfortran", N=1000
        ),
        "Fortran (ifort)": read_benchmark_series(
            BENCHMARKS / "benchmark_sparse_cheby.csv", "QDYN_ifort", N=1000
        ),
        "Julia": read_benchmark_series(
            BENCHMARKS / "benchmark_sparse_cheby.csv", "timing", N=1000
        ),
    }
    properties = {
        "Fortran (gfortran)": dict(marker="^"),
        "Fortran (ifort)": dict(marker="^"),
        "Julia": dict(marker="o"),
    }

    outfile = Path(__file__).with_suffix(".pdf")

    kwargs = dict(
        ylim=(0, 12),
        title="sparse matrices (N = 1000); propagation over 1000 time steps (randomized pulses)",
        step=2,
        minor=2,
    )
    print(f"Generating {outfile}")
    fig = plot_benchmark(data, properties, **kwargs)
    fig.savefig(outfile, transparent=True)

    for frame in [1, 2, 3]:
        outfile_frame = outfile.with_stem(f"{outfile.stem}_{frame}")
        print(f"Generating {outfile_frame}")
        fig = plot_benchmark(
            data,
            properties,
            frame=frame,
            **kwargs,
        )
        fig.savefig(outfile_frame, transparent=True)


if __name__ == "__main__":
    main()
