from bronze.pipeline import main as bronze_pipeline
from silver.pipeline import main as silver_pipeline


def main() -> None:
    bronze_pipeline()
    silver_pipeline()


if __name__ == "__main__":
    main()
