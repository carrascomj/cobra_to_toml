"""Take a set of reactions and translate them to a Maud TOML input."""
from functools import reduce

import cobra
import toml


def reactions_to_toml(reactions: list[cobra.Reaction]) -> str:
    """Convert `cobra.Reaction`s to a maud-like TOML."""
    model = next(r.model for r in reactions)
    # metabolites might appear in more than one reaction but must be specified
    # just once in the TOML file (for each compartment)
    metabolites = set(
        reduce(lambda x, y: x + list(y.keys()), [r.metabolites for r in reactions], [])
    )
    compartments = {m.compartment for m in metabolites}
    if model:
        compartments_dict = [
            {"id": k, "name": v, "volume": 1}
            for k, v in model.compartments.items()
            if k in compartments
        ]
    else:
        compartments_dict = [{"id": k, "name": "", "volume": 1} for k in compartments]
    # metabolites are balanced by default, let the users handle that manually
    metabolites_dict = [
        {
            "metabolite": met.id,
            "name": met.name,
            "compartment": met.compartment,
            "balanced": True,
        }
        for met in metabolites
    ]
    # modifiers are not added, let the users add them themselves
    reactions_dict = [
        {
            "id": reac.id,
            "name": reac.name,
            "stoichiometry": {met.id: coeff for met, coeff in reac.metabolites.items()},
            "mechanism": "reversible_modular_rate_law"
            if reac.reversibility
            else "irreversible_modular_rate_law",
            # WARNING: this is probably a bit too much
            "enzyme": [
                {
                    "id": g.annotation["uniprot"]
                    if "uniprot" in g.annotation
                    else g.id,
                    "name": f"{g.id} in {reac.id}",
                }
                for g in reac.genes
            ],
        }
        for reac in reactions
    ]
    return toml.dumps(
        {
            "compartment": compartments_dict,
            "metabolite-in-compartment": metabolites_dict,
            "reaction": reactions_dict,
        }
    )


def model_to_toml(model: cobra.Model) -> str:
    """Convert `cobra.Model` to a maud-like TOML."""
    return reactions_to_toml(model.reactions)
