from pathlib import Path
from benchmarkplots import read_benchmark_series, plot_benchmark

BENCHMARKS = Path("benchmarks")


def main():

    data = {
        "Fortran (gfortran)": read_benchmark_series(
            BENCHMARKS / "benchmark_dense_cheby.csv", "QDYN_gfortran", N=1000
        ),
        "Fortran (ifort)": read_benchmark_series(
            BENCHMARKS / "benchmark_dense_cheby.csv", "QDYN_ifort", N=1000
        ),
        "Julia": read_benchmark_series(
            BENCHMARKS / "benchmark_dense_cheby.csv", "timing", N=1000
        ),
        "Julia (GPU)": read_benchmark_series(
            BENCHMARKS / "benchmark_gpu_cheby.csv", "timing", N=1000
        ),
    }
    properties = {
        "Fortran (gfortran)": dict(marker="^"),
        "Fortran (ifort)": dict(marker="^"),
        "Julia": dict(marker="o"),
        "Julia (GPU)": dict(marker="o"),
    }

    outfile = Path(__file__).with_suffix(".pdf")

    kwargs = dict(
        ylim=(0, 40),
        title="dense matrices (N = 1000); propagation over 1000 time steps (randomized pulses)",
        step=10,
        minor=2,
    )
    print(f"Generating {outfile}")
    fig = plot_benchmark(data, properties, **kwargs)
    fig.savefig(outfile, transparent=True)

    for frame in [1, 2, 3, 4]:
        outfile_frame = outfile.with_stem(f"{outfile.stem}_{frame}")
        print(f"Generating {outfile_frame}")
        fig = plot_benchmark(data, properties, frame=frame, **kwargs)
        fig.savefig(outfile_frame, transparent=True)


if __name__ == "__main__":
    main()
