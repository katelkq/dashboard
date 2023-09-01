Maintainence
============

This documentation is generated using Sphinx. Go to https://www.sphinx-doc.org/en/master/index.html for details on how to use the package.

In general, though, one might be able to make the desired changes just by looking at the existing stuff...


Building the documentation
--------------------------

Run the following commands within the main folder:

.. code-block:: console

    $ cd docs
    $ ./make html

This will re-build the documentation to reflect the latest changes; the target files are available under :code:`./docs/build/`.

.. warning::

    When building the documentation, all the scripts under :code:`./Dashboard/`, in particular :code:`params_update.py`, will be executed. This will override any manual changes to files under :code:`./Dashboard/lib/`. Watch out!

Note that other output formats are possible; see https://www.sphinx-doc.org/en/master/usage/builders/index.html#builders.


Resources
---------

Here are some potentially useful things to look at.

- A quick reference guide of reStructuredText:
    - https://docutils.sourceforge.io/docs/user/rst/quickref.html
