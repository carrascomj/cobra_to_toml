cobra_to_toml
=============
Convert a cobrapy_'s `cobra.Model` to a
TOML file that can be read by Maud_:

.. code-block:: python

   from cobra_to_toml import model_to_toml


   toml_file = model_to_toml(cobra_model)
   redeserialized = toml.loads(toml_file)

or, most likely, a list of `cobra.Reaction`:

.. code-block:: python

   from cobra_to_toml import reactions_to_toml


   reactions = [cobra_model.reactions.PFK, cobra_model.reactions.PFF]
   toml_file = reactions_to_toml(reactions)
   redeserialized = toml.loads(toml_file)

Additionally, the stoichiometric consistency (adapted from memote_ and, thus, `Gevorgyan et at., 2008`_):


.. code-block:: python

   import cobra_to_toml.stoichiometry as st


   assert st.check_stoichiometric_consistency_from_toml("path/kinetic_model.toml")

Installation
------------

Please install it with

.. code-block:: bash

   pip install git+https://github.com/carrascomj/cobra_to_toml.git#egg=cobra_to_toml

.. _cobrapy: https://github.com/opencobra/cobrapy
.. _Maud: https://github.com/biosustain/Maud
.. _memote: https://github.com/opencobra/memote
.. _Gevorgyan et at., 2008: https://doi.org/10.1093/bioinformatics/btn425
