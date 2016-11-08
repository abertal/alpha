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

Comunícate con nosotros
-----------------------

Hemos creado un grupo en Telegram, si lo deseais, teneis alguna idea o duda, no
dudeis en instalarlo y preguntar

Se puede hacer de varias maneras:

- Si lo queréis en el móvil, solo debereis descargar la aplicación Telegram 
(Tanto en iOs como en Android)
- Si lo queréis en el ordenador, aquí os dejo el enlace de descarga: https://telegram.org/
donde podréis descargar la versión que necesiteis (ya sea PC, Linux, Mac...)

Una vez descargado, tendreis que poner vuestro número de teléfono para darse de alta, y poneros 
un alias.

Cuando termineis con la configuración, solo deberéis buscar el grupo alpha_desarrollo o hacer
click en el siguiente enlace https://telegram.me/joinchat/Ch6vgAmZkCdB1v0_VB3uQA y ya podréis
poneros en contacto con nosotros.

Os esperamos!
