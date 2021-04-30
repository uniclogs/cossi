Quick Start
===========

Install Locally
---------------

`$` `pip install -e .[dev]`

*(Note: the `-e` flag creates a symbolic-link to your local development version. Set it once, and forget it)*

Create Documentation
--------------------

`$` `make -C docs clean html`


Examples
--------

In order to use COSI, it requires a known NORAD ID of an active satellite that is at least registered in `SatNOGS <https://db.satnogs.org>`_ if you wish to grab satellite metadata and telemetry and `Space-Track <https://www.space-track.org>`_ if you wish to grab a satellite's latest TLE's.

.. seealso:: To register a new satellite with SatNOGS, see their `guide on registration <https://wiki.satnogs.org/Satellite_Operator_Guide#2.2_Add_a_new_Mission>`_

.. code-block:: bash

  ## Get Latest TLE for Bobcat-1 (NORAD ID: 46922)
  uniclogs-cosi --tle 46922

  ## Get Satellite Metadata and telemetry for Bobcat-1
  uniclogs-cosi --satellite --telemetry 46922

  ## Get Telemetry for OreFlat0 in SatNOGS DB Dev and decode it using the OreFlat0 decoder
  uniclogs-cosi --telemetry --decode --satnogs-dev 99910
