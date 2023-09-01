Getting Started
===============

Installing dependencies
-----------------------

Run the following command within the main folder:

.. code-block:: console

    $ pip install -r ./requirements.txt


Updating the pickles
--------------------

Run the following command within the main folder:

.. code-block:: console

    $ python ./Dashboard/params_update.py

This will refresh all the pickles under :code:`./Dashboard/lib/` using data freshly fetched from Refinitiv. I don't think this needs to be done very often, though.


Serving the dashboard on a local machine
----------------------------------------

Run the following command within the main folder:

.. code-block:: console

    $ bokeh serve --show Dashboard

