"""Functionality for formatting a protein dataset as priors."""

import re
import warnings

import numpy as np
import pandas as pd
import toml


CAMEL_PATTERN = re.compile(r"([^A-Z])([A-Z]| |\-)")


def extract_prots_maud(maud_toml: str) -> list[str]:
    """Extract the proteins from a maud TOML config."""
    with open(maud_toml) as f:
        config = toml.load(f)
    # the ids correspond to genes in this specific model
    return [prot["id"] for reac in config["reaction"] for prot in reac["enzyme"]]


def format_enzyme_priors(df: pd.DataFrame, protein_ids: list) -> pd.DataFrame:
    """Format a dataset as `conc_enzyme` priors for maud.

    Parameters
    ----------
    df: pd.DataFrame
        columns Gene/proteinID | condition | mM | logSD
    protein_ids: list
        protein/gene identifiers to filter the dataframe

    Warnings
    --------
    It will yell at the proteins that were not in the dataframe.
    """
    df_filter = df[df["Gene/proteinID"].isin(protein_ids)]
    not_found = set(protein_ids) - set(df_filter["Gene/proteinID"].unique())
    if not_found:
        warnings.warn(f"{not_found} were not in the dataframe.")
    return pd.DataFrame(
        {
            "parameter_type": "conc_enzyme",
            "metabolite_id": None,
            "mic_id": None,
            "enzyme_id": df_filter["Gene/proteinID"],
            "drain_id": None,
            "phos_enz_id": None,
            "experiment_id": df_filter["condition"].apply(
                lambda x: re.sub(CAMEL_PATTERN, r"\1_\2", x)
                .lower()
                .replace(" ", "")
                .replace("-", "")
            ),
            "location": df_filter["mM"].round(9),
            "scale": df_filter["logSD"].round(9),
            "pct1": None,
            "pct99": None,
        }
    )


def convert_valgepea_2021_supp_3(supp_table: str) -> pd.DataFrame:
    """Convert the supp table 3 from Valgepea et al., 2021.

    The input file is supposed to be the Supp. table without padding, rank and
    annotations.
    """
    df = pd.read_csv(supp_table, sep="\t", header=[0, 1, 2])
    # fill merged cells from multindex columns
    df.columns = pd.MultiIndex.from_tuples(_unroll_multi_column(df)).droplevel(0)
    # set metadata columns as index to preserve them after the melt
    df_idx = df.set_index(df.columns[:4].to_list())
    # tidy
    df_idx = df_idx.melt(
        var_name=["condition", "stat"], value_name="nmol/gDCW", ignore_index=False
    ).reset_index()
    df_idx.columns = [
        col[1] if isinstance(col, tuple) else col for col in df_idx.columns
    ]
    # now: Gene/ProteinID | ... | ... | condition | stat | nmol/gDCW
    # unmelt the stat -> (AVG | SD)
    df_format = df_idx.pivot(list(df_idx.columns[:5]), "stat").reset_index()
    df_format.columns = [
        col[1] if col[1] in ["AVG", "SD"] else col[0] for col in df_format.columns
    ]
    df_format = df_format.rename({"AVG": "nmol/gDCW"}, axis=1)
    # unit conversion: nnmol/gDCW -> mM (1.4 is gDCW/L for syngas)
    df_format["mM"] = df_format["nmol/gDCW"] * 1e-6 * 1.4
    # unit conversion: normal std -> log normal scale
    df_format["logSD"] = np.sqrt(
        np.log(1 + (df_format["SD"] ** 2) / (df_format["nmol/gDCW"] ** 2))
    )
    return df_format


def _unroll_multi_column(df: pd.DataFrame) -> list[tuple[str, str, str]]:
    cols = df.columns
    new_cols = []
    carries = [None for _ in df.columns[0]]
    for col in cols:
        carries = tuple(
            [
                carry if "Unnamed" in level else level
                for carry, level in zip(carries, col)
            ]
        )
        new_cols.append(carries)
    return new_cols
