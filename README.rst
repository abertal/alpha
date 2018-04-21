=============
alpha project
=============

.. image:: https://travis-ci.org/abertal/alpha.svg?branch=master
    :target: https://travis-ci.org/abertal/alpha

.. image:: https://codecov.io/gh/abertal/alpha/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/abertal/alpha

**alpha project** is proof of concept of a web application to manage an
association day-to-day operations.

You are free to copy, modify, and distribute **alpha project** with attribution
under the terms of the BSD 3-Clause License. See the LICENSE file for details.

This project uses Spanish as the communication language.

Cómo colaborar
==============

Pre requisitos
--------------

- Instalar python 3.6

- Instalar nodejs y yarn

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
    (.venv) $ yarn install

Instrucciones instalación en Windows
------------------------------------

.. code::

    PS > cd alpha
    PS > python3 -m venv .venv
    PS > .venv\Scripts\Activate.PS1
    (.venv) PS > pip install --upgrade pip setuptools wheel
    (.venv) PS > pip install --requirement requirements.txt
    (.venv) PS > pip install --requirement dev-requirements.txt
    (.venv) PS > yarn install

Clonación del repositorio y subida de repositorios
--------------------------------------------------

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


Borrado de ramas y su remote
----------------------------


Volvemos a la rama master,tras hacer pullrequest, en caso de que no lo estemos:

.. code::

    $ git checkout master

Traemos los cambios del repositorio original:

.. code::

    $ git fetch abertal

y ponemos al día nuestro master:

.. code::

    $ git merge --ff-only abertal/master

Una vez el master esta actualizado, procedemos a borrar la rama:

.. code::

    $ git branch --delete nombre_de_la_rama

Además hay que borrar la rama en el remoto:

.. code::

    $ git push origin --delete nombre_de_la_rama


Finalmente, actualizamos nuestro fork en el remoto (nuestro fork en el pc está actualizado desde el git merge anterior):

.. code::

    $ git push origin master

Migraciones de modelos (Windows)
--------------------------------

Primero debemos generar un fichero con los cambios realizados usando PowerShell

.. code::

    > python .\manage.py makemigrations


Para realizar el cambio de modelo y actualizarlo con el fichero generado antes

.. code::

    > python .\manage.py migrate

Migraciones de modelos (Linux)
------------------------------

.. code::

    (.venv) $ python manage.py makemigrations
    (.venv) $ python manage.py migrate


Tests y calidad de código
-------------------------

Antes de enviar un cambio hay que comprobar que el código sigue las
recomendaciones de estilo del estándar PEP8_ ejecutando el comando `flake8`.

.. code::

    (.venv) PS > flake8

Si hay algún error debe corregirse antes.

Lo mismo con el código escrito en Javascript. En este caso se utiliza la
herramienta `eslint`.

.. code::

    (.venv) PS > yarn run lint

También hay que comprobar que no hay errores en los tests. Para ejecutar los
tests simplmente hay que ejecutar el comando `pytest`.

.. code::

    (.venv) PS > pytest

.. attention::

    Algunas pruebas necesitan usar el validador **Nu Html Checker**. Por defecto, la aplicación usa
    el validador público y gratuito https://validator.w3.org/nu/.

También es preciso ejecutar la utilidad `isort` para que las importaciones de
paquetes y librerías estén ordenados y agrupados de manera homogénea en toda la aplicación.

.. code::

    (.venv) PS > isort

.. _PEP8: https://www.python.org/dev/peps/pep-0008/

Instalación de Nu Html Checker en local
---------------------------------------

El validador de HTML Nu Html Checker (v.Nu) está disponible como un servicio
en https://checker.html5.org, https://html5.validator.nu o
https://validator.w3.org/nu.

El código fuente está disponible en https://github.com/validator/validator y
se puede Instalar y ejecutar en tu propio ordenador. Es necesario tener
instalado en el ordenador la versión dede Java 8.

Para ejecutarlo en local, hay que bajar la última versión del archivo
`vnu.jar` y ejecutar:
.. code::

    java -cp vnu.jar nu.validator.servlet.Main 8888

Este comando ejecuta el servidor en la dirección local http://localhost:8888/.

Para que la validación HTML de los tests se haga contra nuestro servidor
local es necesario indicar la dirección local usando una variable de
entorno/..

En **Windows**:

.. code::

    (.venv) PS > set-variable -name HTMLVALIDATOR_VNU_URL -value "http://localhost:8888/"
    (.venv) PS > pytest


En **Linux**:

.. code::

    (.venv) $ HTMLVALIDATOR_VNU_URL=http://localhost:8888/ pytest


Hay más información en `html5validation`_.

.. _html5validation: html5validation/README.rst

Guía de estilo: HTML
--------------------

1. La indentación es de 2 espacios.

2. Las etiquetas de Django **no** incrementan la indentación (por ejemplo `{% if %}`).

3. Los elementos HTML sí que añaden un nivel de indentación.

4. Excepción: `<html>`, `<head>` y `<body>`

Un ejemplo:

.. code::html

    <html>
    <body>
    <ul>
      {% if condition %}
      {% for item in menu_item %}
      <li>{{ item }}</li>
      {% endfor %}
      {% endif %}
    </ul>
    <main>
      {% block content %}
      <p>Hello World</p>
      {% endblock content %}
    </main>
    </body>
    </html>

Para el resto de aspectos (atributos, cierre de elementos...) se utiliza como referencia http://codeguide.co/.
