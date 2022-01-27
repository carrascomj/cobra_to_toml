"""Test stoichiometry functionality."""

import pandas as pd

from cobra_to_toml.proteomics import format_enzyme_priors


def test_proteomics_prior_conversion_has_right_dims(proteomics_file: str):
    """Test model conversion returns the right number of redeserialized components."""
    proteins = [
        "CAETHG_RS16490",
        "CAETHG_RS16495",
        "CAETHG_RS00440",
        "CAETHG_RS08920",
        "ETOH_UNK",
        "AC_UNK",
        "CAETHG_RS14890",
    ]
    proteins_in_df = [
        "CAETHG_RS16490",
        "CAETHG_RS16495",
        "CAETHG_RS00440",
        "CAETHG_RS08920",
        "CAETHG_RS14890",
    ]
    df = format_enzyme_priors(
        pd.read_csv(proteomics_file, sep="\t"),
        proteins,
    )
    assert len(df["enzyme_id"].unique()) == len(proteins_in_df)
    assert len(df["experiment_id"].unique()) * len(proteins_in_df) == df.shape[0]


def test_proteomics_prior_conversion_has_right_types(proteomics_file: str):
    """Test model conversion returns the right number of redeserialized components."""
    proteins = [
        "CAETHG_RS16490",
        "CAETHG_RS16495",
        "CAETHG_RS00440",
        "CAETHG_RS08920",
        "CAETHG_RS14890",
    ]
    df = format_enzyme_priors(
        pd.read_csv(proteomics_file, sep="\t"),
        proteins,
    )
    # assert numeric types
    assert pd.api.types.is_numeric_dtype(df.location.dtype)
    assert pd.api.types.is_numeric_dtype(df.scale.dtype)
    # check snake cases
    assert df.experiment_id.str.islower().all()
    assert not df.experiment_id.str.contains(" ").any()
