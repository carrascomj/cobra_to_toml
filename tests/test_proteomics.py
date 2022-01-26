"""Test stoichiometry functionality."""

import pandas as pd

from cobra_to_toml.proteomics import format_enzyme_priors


def test_proteomics_prior_conversion(proteomics_file: str):
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
