"""Test stoichiometry functionality."""

import inspect
import os

import cobra

from cobra_to_toml import reactions_to_toml
from cobra_to_toml.stoichiometry import check_stoichiometric_consistency_from_toml


def test_consistent_set_of_reactions(cobra_model: cobra.Model):
    """Test model conversion returns the right number of redeserialized components."""
    toml_file = reactions_to_toml(
        [cobra_model.reactions.PFK, cobra_model.reactions.FBA]
    )
    filename = f"{inspect.stack()[0][3]}.toml"
    with open(filename, "w") as file:
        file.write(toml_file)
    assert check_stoichiometric_consistency_from_toml(filename)
    os.remove(filename)
