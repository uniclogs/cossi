Development Reference
=====================

A development reference for CoSSI.


Compile A Decoder
-----------------

**In order to add or update a decoder in CoSSI:**

1. A Valid Kaitai Structure
2. Kaitai Struct Compiler

.. seealso:: See the `Kaitai website <https://kaitai.io/#download>`_ for information on installing the kaitai-struct-compiler.

Place the desired kaitai structure in the `./ksy/` directory.

Once both items are acquired, run the following:

.. code-block:: bash

    ## Compile the structure and write the output to cosi/decoders/
    $ kaitai-struct-compiler --target python --outdir cosi/decoders ksy/<your struct>.ksy

If this overwrites a previously compiled decoder, then no further action is needed, assuming the actions to add a new decoder have already been done.

Add A Newly Compiled Decoder
----------------------------

If the previous steps generate a wholly new decoder, then some additional steps are needed to ensure it gets used by CoSSI.

First, the `cosi.decoders` module needs to be updated to include your newly generated python module.

.. code-block:: python

    cosi/decoders/__init__.py
    -------------------------

    from .csim import Csim
    from .oreflat0 import Oreflat0
    from .`new decoder name` import `new decoder class`

    __all__ = [
        "Csim",
        "Oreflat0",
        "`new decoder class`"
    ]


Once this is done, it's up to you to write a new decoder function in the `cosi.satnogs` module. Since the process involves any arbitrary kaitai struct, the method in which you read the decoded data back is also arbitrary.


Example Kaitai Struct
---------------------

This is an example of what a vaild Kaitai Structure might look like. This structure uses `ax.25` encoding and expects a valid callsign in the header. It has a 67 byte ASCII field for a payload.

.. literalinclude:: ../ksy/oreflat0.ksy
  :language: text


CoSSI Reference
---------------

.. automodule:: cosi
   :members:
   :private-members:

SatNOGS Reference
-----------------

.. automodule:: cosi.satnogs
   :members:
   :private-members:

SpaceTrack Reference
--------------------

.. automodule:: cosi.spacetrack
   :members:
   :private-members:
