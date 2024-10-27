import pandas as pd
import os
import numpy as np
from sdv.metadata import SingleTableMetadata
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.evaluation.single_table import run_diagnostic, evaluate_quality, get_column_plot

def combine_columns(data):
    # If "start", "end" and "bus_num" are in separate columns, synthesised data may have nonsensical data (eg. "start" and "end" being the same). So we need to combine these 3 columns into one single column, "trip"
    data = data.copy()
    data["trip"] = data[["start", "end", "bus_num"]].agg(",".join, axis=1)

    # Remove "start", "end" and "bus_num" columns
    data.drop(columns=["start", "end", "bus_num"], inplace=True)
    return data


def create_metadata(data):
    # Initialise and populate metadata
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(data)

    # Update metadata - because some columns have incorrect types
    metadata.update_column(column_name="time", sdtype="datetime", datetime_format="%Y-%m-%d %H:%M:%S")
    metadata.update_column(column_name="trip", sdtype="categorical")
    return metadata


def generate_synthetic_data(data, metadata):
    synthesiser = GaussianCopulaSynthesizer(metadata)
    synthesiser.fit(data)

    # Generate 1160 rows of synthetic data
    synthetic_data = synthesiser.sample(num_rows=1160) 
    return synthetic_data


def diagnose_synthetic_data(data, synthetic_data, metadata):
    diagnostic = run_diagnostic(data, synthetic_data, metadata)
    return diagnostic


def assess_synthetic_data_quality(data, synthetic_data, metadata):
    quality_report = evaluate_quality(data, synthetic_data, metadata)
    return quality_report


def plot_similarity(data, synthetic_data, metadata, col_name):
    # Plot graphs to compare real data and synthetic data
    fig = get_column_plot(data, synthetic_data, metadata, col_name)
    fig.show()


def edit_synthetic_data(synthetic_data):
    # Split "trip" column back into "start", "end" and "bus_num"
    synthetic_data[["start", "end", "bus_num"]] = synthetic_data["trip"].str.split(",", expand=True)
    synthetic_data.drop("trip", axis=1, inplace=True)

    # Rearrange columns
    synthetic_data = synthetic_data[["year", "major", "on_campus", "main_reason_for_taking_isb", "trips_per_day", "duration_per_day", "date", "has_exam", "start", "end", "bus_num", "time", "weather", "num_people_at_bus_stop", "waiting_time", "waiting_time_satisfaction", "crowdedness", "crowdedness_satisfaction", "comfort", "safety", "overall_satisfaction"]]

    # Extract only the date for "date" column
    synthetic_data["date"] = synthetic_data["date"].map(lambda date: date.date())

    return synthetic_data


def main():
    np.random.seed(42)
    trip_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test_trip_data_before_sdv.csv"), keep_default_na=False)

    # Combine "start", "end", "bus_num" into "trip"
    real_data = combine_columns(trip_data)

    # Create and save metadata that is to be used for synthesis
    # metadata = create_metadata(real_data)
    # metadata.save_to_json(os.path.join(os.path.dirname(__file__), "../data/sdv_metadata.json"))

    # Load existing metadata that is to be used for synthesis
    metadata = SingleTableMetadata.load_from_json(os.path.join(os.path.dirname(__file__), "../data/sdv_metadata.json"))

    # Synthesise data
    synthetic_data = generate_synthetic_data(real_data, metadata)

    # Check validity of synthetic data
    diagnostic = diagnose_synthetic_data(real_data, synthetic_data, metadata)

    # Plot graphs to compare synthetic data and original trip data
    # plot_similarity(real_data, synthetic_data, metadata, "major")

    # Check quality of synthetic data
    quality_report = assess_synthetic_data_quality(real_data, synthetic_data, metadata)

    # Change synthetic data to match original trip data
    synthetic_data = edit_synthetic_data(synthetic_data)

    # Stacking original trip data and synthetic trip data on top of each other
    combined_trip_data = pd.concat([trip_data, synthetic_data], ignore_index=True)

    # Save combined trip data
    combined_trip_data.to_csv(os.path.join(os.path.dirname(__file__), "../data/test_trip_data_after_sdv.csv"), index=False)


if __name__ == "__main__":
    main()
