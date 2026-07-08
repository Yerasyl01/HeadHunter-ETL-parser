import itertools
import shutil
import polars as pl
from collections.abc import Iterator
from pathlib import Path
from db.mongo import mongodb
from silver.transformer import HHVacancyTransformer
from bronze.normalize import normalize

def read_bronze(batch_size: int = 10000) -> Iterator[pl.DataFrame]:
    cursor = mongodb.raw_vacancies.find()
    while True:
        batch = list(itertools.islice(cursor, batch_size))
        if not batch:
            break
        yield pl.DataFrame([normalize(doc) for doc in batch])

def main() -> None:
    mongodb.connect()
    transformer = HHVacancyTransformer()

    output_dir = Path("data/vacancies")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    total_rows = 0
    for batch_number, bronze_batch in enumerate(read_bronze()):
        silver = transformer.transform(bronze_batch)

        output_path = output_dir / f"part-{batch_number:05}.parquet"
        silver.write_parquet(output_path)

        total_rows += silver.height
        print(
            f"Written batch {batch_number} "
            f"({silver.height} rows) -> {output_path}"
        )
    print(f"\nDone. Total rows written: {total_rows}")

if __name__ == "__main__":
    main()
