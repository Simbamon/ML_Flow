import mlflow.data
import pandas as pd
from mlflow.data.pandas_dataset import PandasDataset
import datetime

output_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
# Construct a Pandas DataFrame using iris flower data from a web URL
dataset_source_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
df = pd.read_csv(dataset_source_url, delimiter=";")

# Construct an MLflow PandasDataset from the Pandas DataFrame, and specify the web URL
# as the source
dataset: PandasDataset = mlflow.data.from_pandas(df, source=dataset_source_url)

# Set our tracking server uri for logging
mlflow.set_tracking_uri(uri="http://localhost:8080")

# Create a new MLflow Experiment
mlflow.set_experiment("MLflow Data Versioning")

with mlflow.start_run():
    # Log the dataset to the MLflow Run. Specify the "training" context to indicate that the
    # dataset is used for model training
    mlflow.log_input(dataset, context=output_date)

# Retrieve the run, including dataset information
run = mlflow.get_run(mlflow.last_active_run().info.run_id)
dataset_info = run.inputs.dataset_inputs[0].dataset
print(dataset_info)
print(f"Dataset name: {dataset_info.name}")
print(f"Dataset digest: {dataset_info.digest}")
print(f"Dataset profile: {dataset_info.profile}")
print(f"Dataset schema: {dataset_info.schema}")

# Load the dataset's source, which downloads the content from the source URL to the local
# filesystem
dataset_source = mlflow.data.get_source(dataset_info)
dataset_source.load()