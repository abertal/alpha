==============
Proyecto alpha
==============

Manual de uso
=============

Importación de datos
--------------------

En alpha se pueden importar datos desde un archivo en formato XLSX utilizando un comando.

.. code::

    $ python manage.py importdata master.xlsx

Generación de archivos de traducción
------------------------------------

Para generar los archivos de traducción es necesario utilizar el siguiente comando que devolverá todas las cadenas susceptibles a traducción.

..code::
    $ python manage.py makemessages

Esto generará un django.po que puede ser editado con un programa de edición de archivos .po (POEdit por ejemplo):
https://poedit.net/

En nuestro proyecto utilizamos los idiomas castellano y gallego. Aquí la referencia a estos idiomas:
https://digalego.xunta.gal/digalego/Html/index.php
http://dle.rae.es/?w=diccionario

Una vez editado el archivo .po es necesario hacer la compilación del archivo binario que mostrará las cadenas ya traducidas:

..code::
    $python manage.py compilemessages
