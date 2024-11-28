from datasets import load_dataset
import os


class DataLoader:
    """
    A simple DataLoader for text data stored in csv files.
    """

    def __init__(self, data_path, columns=None, batch_size=32, test_size=None):
        """
        Initialize the DataLoader with the path to the training data and batch size.

        Args:
            data_path (str): Path to the folder containing csv files.
            columns (list): List of columns to load from the csv files.
        """
        self.batch_size = batch_size
        self.columns = columns
        self._load_data(data_path)
        if test_size:
            self.dataset = self.dataset.train_test_split(test_size=test_size)

    def _load_data(self, data_path: str):
        """
        Load multiple csv files from a given path and create a Hugging Face Dataset.
        """

        try:
            assert os.path.exists(data_path)
        except AssertionError:
            print(f"Data path does not exist: {data_path}")
            raise FileNotFoundError(f"Data path does not exist: {data_path}")

        data_files = [os.path.join(data_path, f) for f in os.listdir(data_path) if f.endswith(".csv")]
        self.dataset = load_dataset(
            "csv",
            data_files=data_files,
            split="train",
        )
        if self.columns:
            self.dataset = self.dataset.select_columns(self.columns)
        print(f"Loaded {len(self.dataset)} samples from {self.dataset}.")

    def __iter__(self):
        """
        Iterate over the dataset and yield batches of text data.
        """
        for batch in self.dataset.iter(batch_size=self.batch_size):
            if self.columns and len(self.columns) == 1:
                yield batch[self.columns[0]]
            else:
                yield batch
