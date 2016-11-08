=============
alpha project
=============

**alpha project** is proof of concept of a web application to manage an
association day-to-day operations.

You are free to copy, modify, and distribute **alpha project** with attribution
under the terms of the BSD 3-Clause License. See the LICENSE file for details.

This project uses Spanish as the communication language.

Cómo colaborar
==============

Pre requisitos
--------------

- Instalar python 3.5

- Instalar y configurar git

Instrucciones instalación en Mac/Linux
--------------------------------------

.. code::

    $ git clone https://github.com/abertal/alpha.git
    $ cd alpha
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    (.venv) $ pip install --upgrade pip setuptools wheel
    (.venv) $ pip install --requirement requirements.txt
    (.venv) $ pip install --requirement dev-requirements.txt

Instrucciones instalación en Windows
------------------------------------

.. code::

    PS > cd alpha
    PS > python3 -m venv .venv
    PS > .venv\Scripts\Activate.PS1
    (.venv) PS > pip install --upgrade pip setuptools wheel
    (.venv) PS > pip install --requirement requirements.txt
    (.venv) PS > pip install --requirement dev-requirements.txt

Clonación del repositorio
-------------------------

Hay que crear una carpeta, donde clonaremos el repositorio.
Desde el bash de git, nos ubicamos en la carpeta que acabamos de crear.

.. code::

    git clone https://github.com/TuUsuarioGitHub/alpha.git

Comprobamos que no haya modificaciones pendientes

.. code::

    git status

Para trabajar , creamos un rama para no modificar el repositorio original

.. code::
    git branch NombreDeLaRama

Nos cambiamos a la rama creada

.. code::
    git checkout ramauno

Para añadir cambios a la rama

.. code::
    git add FicherosModificados

Para guardar los cambios en la rama

.. code::
    git commit

Para subir los cambios a la rama

.. code::
    git push origin NombreDeLaRama

Tests y calidad de código
-------------------------

Antes de enviar un cambio hay que comprobar que el código sigue las
recomendaciones de estilo del estándar PEP8_ ejecutando el comando `flake8`.

.. code::

    (.venv) PS > flake8

Si hay algún error debe corregirse antes.

También hay que comprobar que no hay errores en los tests. Para ejecutar los
tests simplmente hay que ejecutar el comando `pytest`.

.. code::

    (.venv) PS > pytest

Al igual que con la comprobación anterior, no se puede subir código que no pase
los tests.

.. _PEP8: https://www.python.org/dev/peps/pep-0008/
