from pathlib import Path

import pandas as pd


def load_kaggle_csv(dataset: str, file_path: str, encoding: str) -> pd.DataFrame:
    """Read one CSV file from a Kaggle dataset and return it unchanged.

    The whole dataset is downloaded as one compressed archive and cached by kagglehub,
    so later reads of other files in the same dataset do not download again. Public
    datasets work anonymously; KAGGLE_USERNAME and KAGGLE_KEY are used when set.
    """
    if not file_path.strip():
        raise ValueError("file_path must name a file inside the Kaggle dataset")

    # Keep the Kaggle client out of API imports; only pipeline runs need it.
    import kagglehub  # pylint: disable=import-outside-toplevel

    dataset_dir = Path(kagglehub.dataset_download(dataset))
    csv_path = dataset_dir / file_path
    if not csv_path.is_file():
        available = sorted(p.name for p in dataset_dir.iterdir())
        raise FileNotFoundError(f"{file_path} is not in {dataset}. Available files: {available}")
    return pd.read_csv(csv_path, encoding=encoding)
