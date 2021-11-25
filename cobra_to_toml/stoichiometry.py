"""Stoichiometry operations from a maud TOML file."""

import logging

import cobra
import toml
from memote.support.consistency import check_stoichiometric_consistency


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def toml_to_cobra(toml_dict: dict) -> cobra.Model:
    """Build a `cobra.Model` given a TOML representing a Maud model."""
    model = cobra.Model("maud_model")
    model.add_metabolites(
        [
            cobra.Metabolite(
                f"{met['metabolite']}_{met['compartment']}", met["compartment"]
            )
            for met in toml_dict["metabolite-in-compartment"]
        ]
    )
    LOGGER.debug(
        f"{len(model.metabolites)} gathered: {[met.id for met in model.metabolites]}"
    )
    reacs_to_add = []
    for reac_toml in toml_dict["reaction"]:
        reac = cobra.Reaction(
            reac_toml["id"],
        )
        reac.add_metabolites(
            {
                model.metabolites.get_by_id(met): coeff
                for met, coeff in reac_toml["stoichiometry"].items()
            }
        )
        reacs_to_add.append(reac)
    model.add_reactions(reacs_to_add)
    LOGGER.debug(
        f"{len(model.reactions)} gathered: {[reac.id for reac in model.reactions]}"
    )
    return model


def check_stoichiometric_consistency_from_toml(toml_file: str) -> bool:
    """Retrieve stoichiometric from a toml file.

    Parameter
    ---------
    toml_file: str
        path to kinetic model maud-TOML file

    Returns
    -------
    bool
        true if the model is consistent

    Example
    -------

    >>> import cobra_to_toml.stoichiometry as st
    >>>
    >>> assert st.check_stoichiometric_consistency_from_toml("path/to/kinetic.toml")

    """
    with open(toml_file) as file:
        deser_toml = toml.load(file)
    cobra_model = toml_to_cobra(deser_toml)
    return check_stoichiometric_consistency(cobra_model)
