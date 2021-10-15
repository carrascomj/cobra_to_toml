cobra_to_toml
=============
Convert a [cobrapy](https://github.com/opencobra/cobrapy)'s `cobra.Model` to a
TOML file that can be read by [Maud](https://github.com/biosustain/Maud):

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

Installation
------------

Please install it with

.. code-block:: bash

   pip install git+https://github.com/carrascomj/cobra_to_toml.git#egg=cobra_to_toml

