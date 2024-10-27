import pandas as pd
import os
import numpy as np
from sdv.metadata import SingleTableMetadata
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.evaluation.single_table import run_diagnostic, evaluate_quality, get_column_plot


def create_metadata(data):
    # Initialise and populate metadata
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(data)

    # Update metadata - because some columns have incorrect types
    metadata.update_column(column_name="time", sdtype="datetime", datetime_format="%Y-%m-%d %H:%M:%S")
    return metadata


def diagnose_synthetic_data(data, synthetic_data, metadata):
    diagnostic = run_diagnostic(data, synthetic_data, metadata)
    return diagnostic


def assess_synthetic_data_quality(data, synthetic_data, metadata):
    quality_report = evaluate_quality(data, synthetic_data, metadata)
    return quality_report


# Train dataset
train_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data.csv"), keep_default_na=False)

# Test dataset
test_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test_trip_data.csv"), keep_default_na=False)

# Create and save metadata that is to be used for synthesis
# metadata = create_metadata(test_data)
# metadata.save_to_json(os.path.join(os.path.dirname(__file__), "../data/syn_metadata.json"))

# Load existing metadata that is to be used for synthesis
metadata = SingleTableMetadata.load_from_json(os.path.join(os.path.dirname(__file__), "../data/syn_metadata.json"))

# Check validity of train data
diagnostic = diagnose_synthetic_data(test_data, train_data, metadata)

# Check quality of train data
quality_report = assess_synthetic_data_quality(test_data, train_data, metadata)

# Stacking train and test data on top of each other
combined_trip_data = pd.concat([train_data, test_data], ignore_index=True)

# Save combined trip data
combined_trip_data.to_csv(os.path.join(os.path.dirname(__file__), "../data/combined_trip_data.csv"), index=False)