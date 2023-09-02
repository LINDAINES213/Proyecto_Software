# Proyecto_Software

## 👩‍💻 Proceso para correr la aplicación desde tu dispositivo

`Entorno Virtual`: Primero debe asegurarse de tener Python instalado en su computadora. Teniendolo ya instalado en un cmd se debe correr el siguiente comando:
```bash
pip install virtualenv
```
Si deseas confirmar que este se installo correctamente corre el comando a continuación y te debería de mostrar `virtualenv==20.21.0` en la lista. (La version dependera de la fecha en que lo hayas instalado).
```bash
pip freeze
```
`Clonar el repositorio`: Luego de tener ya el entorno virtual instalado puedes proceder a clonar el repositorio con el siguiente comando:
```bash
git clone https://github.com/LINDAINES213/Proyecto_Software.git
``` 
`Configurar Base de Datos`: Dentro del repositorio se encuentra el archivo `Proyecto_software.dump` el cual debes subir como un restore en una base de datos creada en pgAdmin. Luego en la carpeta raiz del proyecto crea el archivo llamado .env, donde lo llenes con el formato a continuacion, debes de cambiar los datos que sean necesarions, como la contraseña, nombre de la base de datos que le colocaste en pgAdmin, usuario, etc. El secret key se debe dejar tal y como esta.
```bash
SECRET_KEY = SOFTWARE_123
PGSQL_HOST = localhost
PGSQL_USER = postgres
PGSQL_PASSWORD = TU_CONTRASEÑA
PGSQL_DATABASE = NOMBRE_BASE_DE_DATOS
```
Igualmente se debe crear el archivo `config.py` se debe colocar en este formato cambiando igualmente los datos necesarios como en el archivo `.env`:
```bash
class Config:
    SECRET_KEY = 'SOFTWARE_123'

class DevelopmentConfig(Config):
    DEBUG = True
    PGSQL_HOST = 'localhost'
    PGSQL_USER = 'postgres'
    PGSQL_PASSWORD = 'TU_CONTRASEÑA'
    PGSQL_DATABASE = 'NOMBRE_BASE_DE_DATOS'

config = {
    'development': DevelopmentConfig
}
```
`Creando el entorno virtual`: Dentro de la carpeta del proyecto, hay un archivo llamado `requirements.txt`. En una terminal dentro de la carpeta raíz del proyecto crea el ambiente virtual con el comando
```bash
python -m venv venv 
```
En este caso la carpeta de tu entorno virtual tendrá de nombre venv. Luego para instalar los requirments del archivo `requirements.txt` se debe ejecutar este comando en la terminal, siempre en la carpeta raíz del proyecto:
```bash  
pip install -r requirements.txt
```
`Corriendo el programa`: Al tener la base de datos ya configurada con la API correctamente deberria de dejar que se pueda correr, por lo que en la terminal, de preferencia que sea de tipo Command Prompt y correr los siquientes comandos:
```bash
.\venv\Scripts\activate
```
Para correr la API:
```bash
python app.py 
```
Con esto la terminal deberia de mostrarse asi <br><br>
![image](https://github.com/LINDAINES213/Proyecto_Software/assets/77686175/90c7468e-4415-4287-8787-a63b33ce8faa)
<br><br>
Donde se muestra el link donde se esta corriendo la aplicacion web y se puede visualizar, el caso de la fotografia es este
```bash
http://127.0.0.1:5000
```
Para el log in de la plataforma dentro del repositorio tambien se adjunta un archivo csv con los usuarios que puede utilizar para probar las funcionalidades.

En caso de no correr correctamente verificar que los pasos anteriores se realizaron correctamente.
