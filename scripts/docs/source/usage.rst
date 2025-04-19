Usage
=====

.. _installation:

Installation
------------

To use arTeX, first install it using pip:

.. code-block:: console

   (.venv) $ pip install lumache



you can use the ``lumache.perform_build_steps()`` function:

.. autofunction:: scripts.compile.compiler.perform_build_steps

>>> import scripts.compile.compiler
>>> scripts.compile.compiler.perform_build_steps()
['shells', 'gorgonzola', 'parsley']