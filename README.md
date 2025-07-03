# DevChallenge
Este es el repositorio para gestión del Proyecto Dev Challenge - App web que apoye el transporte seguro y sostenible para la comunidad universitaria

Instalación del ambiente
Ubuntu Linux / MacOS
Instalación de gestor de ambientes virtuales de Python

sudo apt install python3-venv
Creación del ambiente virtual

python3 -m venv .venv
Activación del ambiente virtual

source .venv/bin/activate
Instalación de dependencias de este proyecto

pip3 install -r requirements.txt
En caso de querer desactivar el ambiente usar

deactivate
Windows
Instalación de gestor de ambientes virtuales de Python

pip install virtualenv
Creación del ambiente virtual

py -m venv .venv
Activación del ambiente virtual para CMD

.venv\Scripts\activate
Activación del ambiente virtual para PowerShell

.venv\Scripts\activate.ps1
Instalación de dependencias de este proyecto

pip install -r requirements.txt
En caso de querer desactivar el ambiente usar

deactivate
Iniciar el servidor
Para inicial el servidor se debe activar el ambiente virtual (revisar paso anterior) ejecutar el siguiente comando

Linux o MaCOS
python3 manage.py runserver
Windows
python manage.py runserver
Una vez inicializado el servidor se deberá dirigir al siguiente enlace: http://localhost:8000

Crear nueva aplicación
Para generar la primera aplicación se deberá ejecutar el siguiente comando

Linux o MaCOS
python3 manage.py startapp pokedex
Windows
python manage.py startapp pokedex
