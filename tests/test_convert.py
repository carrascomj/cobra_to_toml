"""Test converter."""

import cobra
import toml

from cobra_to_toml import model_to_toml, reactions_to_toml


def test_from_model_redeserialization(cobra_model: cobra.Model):
    """Test model conversion returns the right number of redeserialized components."""
    toml_file = model_to_toml(cobra_model)
    redeserialized = toml.loads(toml_file)
    assert len(redeserialized["reactions"]) == len(cobra_model.reactions)
    assert len(redeserialized["metabolites"]) == len(cobra_model.metabolites)
    assert len(redeserialized["compartments"]) == len(cobra_model.compartments)


def test_from_reactions_redeserialization(cobra_model: cobra.Model):
    """Test reaction conversion returns the right number of redeserialized reactions."""
    toml_file = reactions_to_toml(
        [r for i, r in enumerate(cobra_model.reactions) if i % 5 == 0]
    )
    redeserialized = toml.loads(toml_file)
    assert len(redeserialized["reactions"]) == int(len(cobra_model.reactions) / 5)
