"""Session level fixtures."""
from os.path import dirname, join

import cobra
import pytest


@pytest.fixture(scope="session")
def cobra_model() -> cobra.Model:
    """Load from cobrapy (won't be modified so it can be session-level)."""
    return cobra.io.read_sbml_model(
        join(dirname(__file__), "data", "ecoli_core_model.xml")
    )
