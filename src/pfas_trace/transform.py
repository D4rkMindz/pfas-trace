import pandas as pd
import numpy as np

from sklearn.neighbors import BallTree

from pfas_trace.config import DATASET_FILE

def _clean_invalid_records(df: pd.DataFrame) -> pd.DataFrame:
    """Centralizes and controls all cleanups discussed during data exploration.

    Args:
        df (pd.DataFrame): RAW input dataframe to clean.

    Returns:
        pd.DataFrame: cleaned dataframe, ready for feature extraction.
    """
    cleaned_df = df.dropna(subset=["lat", "lon", "date"]) # as stated in 01_DataExploration.ipynb
    return cleaned_df


def _extract_tier1_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts TierA: PFAS-Source Category.
    Answers: How close is a source in each category?

    Features:
    - producer_distance_min
    - producer_count_5km
    - user_distance_min
    - user_count_5km
    - presumptive_distance_min
    - presumptive_count_5km

    Args:
        df (pd.DataFrame): RAW-Input Dataframe

    Raises:
        TypeError: _description_

    Returns:
        pd.DataFrame: Extracted Tier1 features.
    """
    earth_radius_km: float = 6371.0088
    batch_size: int = 10_000
    count_bands_km: tuple[tuple[float, float], ...] = (
        (0.0, 5.0),
        (5.0, 25.0),
        (25.0, 50.0),
    )


    tier1_feature_df: pd.DataFrame = (
        _clean_invalid_records(df)
        .loc[
            df["category"] == "Measurement",
            ["date", "lat", "lon", "name", "city", "pfas_sum"],
        ]
        .copy()
        .reset_index(drop=True)
    )

    producers_df: pd.DataFrame = df.loc[
        df["category"] == "PFAS production facility"
    ]
    users_df: pd.DataFrame = df.loc[
        df["category"] == "Known PFAS user"
    ]
    presumptives_df: pd.DataFrame = df.loc[
        df["category"] == "Presumptive"
    ]

    coordinates: pd.DataFrame = tier1_feature_df[["lat", "lon"]].apply(
        pd.to_numeric, errors="coerce"
    )

    valid_measurements: np.ndarray = (
        coordinates.notna().all(axis=1)
        & coordinates["lat"].between(-90, 90)
        & coordinates["lon"].between(-180, 180)
    ).to_numpy()

    measurement_coords: np.ndarray = np.radians(
        coordinates.to_numpy(dtype=np.float64)
    )

    def add_source_features(
        source_df: pd.DataFrame,
        prefix: str,
    ) -> None:
        """Add nearest-source distance and counts in disjoint distance bands."""

        source_coordinates: pd.DataFrame = source_df[
            ["lat", "lon"]
        ].apply(pd.to_numeric, errors="coerce")

        valid_sources: pd.Series = (
            source_coordinates.notna().all(axis=1)
            & source_coordinates["lat"].between(-90, 90)
            & source_coordinates["lon"].between(-180, 180)
        )

        source_coords: np.ndarray = np.radians(
            source_coordinates.loc[valid_sources].to_numpy(
                dtype=np.float64
            )
        )

        distance_column: str = f"{prefix}_distance_min"
        tier1_feature_df[distance_column] = np.nan

        for lower_km, upper_km in count_bands_km:
            feature_name: str = (
                f"{prefix}_count_{lower_km:g}_{upper_km:g}km"
            )
            tier1_feature_df[feature_name] = np.nan

        valid_indices: np.ndarray = np.flatnonzero(
            valid_measurements
        )

        if len(source_coords) == 0:
            for lower_km, upper_km in count_bands_km:
                tier1_feature_df.loc[
                    valid_indices,
                    f"{prefix}_count_{lower_km:g}_{upper_km:g}km",
                ] = 0
            return

        tree: BallTree = BallTree(
            source_coords,
            metric="haversine",
        )

        for start in range(0, len(valid_indices), batch_size):
            indices: np.ndarray = valid_indices[
                start : start + batch_size
            ]
            batch_coords: np.ndarray = measurement_coords[indices]

            distances_rad, _ = tree.query(batch_coords, k=1)

            distances_km: np.ndarray = (
                distances_rad[:, 0] * earth_radius_km
            )

            tier1_feature_df.loc[indices, distance_column] = distances_km

            # Count sources cumulatively within each upper boundary.
            cumulative_counts: dict[float, np.ndarray] = {}

            for _, upper_km in count_bands_km:
                counts_result = tree.query_radius(
                    batch_coords,
                    r=upper_km / earth_radius_km,
                    count_only=True,
                )

                if isinstance(counts_result, tuple):
                    raise TypeError(
                        "Expected an array from query_radius "
                        "with count_only=True."
                    )

                cumulative_counts[upper_km] = np.asarray(
                    counts_result,
                    dtype=np.int64,
                )

            # Convert cumulative counts into disjoint bands.
            for band_index, (lower_km, upper_km) in enumerate(
                count_bands_km
            ):
                upper_counts: np.ndarray = cumulative_counts[upper_km]

                if band_index == 0:
                    band_counts: np.ndarray = upper_counts
                else:
                    lower_counts: np.ndarray = cumulative_counts[lower_km]
                    band_counts = upper_counts - lower_counts

                tier1_feature_df.loc[
                    indices,
                    f"{prefix}_count_{lower_km:g}_{upper_km:g}km",
                ] = band_counts

    add_source_features(producers_df, "producer")
    add_source_features(users_df, "user")
    add_source_features(presumptives_df, "presumptive")

    return tier1_feature_df

def load_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    feature_df = _extract_tier1_features(df)

    return feature_df
    # CemA, ChemB, PFAS_sum (Label),


    feature_df = df.query('category == "Measurement"')[
        ['year','lat','lon','name','city', 'pfas_sum']
    ]

    producers_df = df.query('category == "PFAS production facility"')
    users_df = df.query('category =="Known PFAS user"')
    presumptives_df = df.query('category == "Presumptive"')






    # TierB: Industrial Sector (How close is a particular type of industry?)
    # metal_coating_distance_min
    # metal_coating_count_5km
    # sewerage_distance_min
    # sewerage_count_5km
    # plastic_manufacturing_distance_min
    # plastic_manufacturing_count_5km


    # TierC: Sourcecategory X Sector

    # Set correct datatypes

    return feature_df
