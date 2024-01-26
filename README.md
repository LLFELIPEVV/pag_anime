# Mi Página de Anime
![Estado de construcción](https://img.shields.io/badge/Estado%20de%20Construcción-En%20Progreso-yellow)
![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-blue)

¡Bienvenido a mi proyecto de página de anime! Este repositorio alberga el código fuente y los recursos de mi plataforma dedicada a los amantes del anime. A continuación, te proporciono una breve guía para entender y contribuir a este proyecto.

## Contenido
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Cómo Contribuir](#cómo-contribuir)
  - [Configuración del Entorno](#configuración-del-entorno)
  - [Instrucciones para la Base de Datos](#instrucciones-para-la-base-de-datos)
  - [Correcciones en la API](#correcciones-en-la-api)
  - [Importar Información de Animes](#importar-información-de-animes)
- [Contacto](#contacto)

## Tecnologías Utilizadas
- **Backend:** Python, Django
- **Base de Datos:** SQL (MySQL)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Otros:** Git, GitHub, SCRUM

## Estructura del Proyecto
El proyecto sigue una arquitectura MVT con el backend construido en Django. Aquí hay una vista rápida de la estructura:
```
/
|-- animes/
|   |-- models.py
|   |-- views.py
|   |-- ...
|-- pagina_anime/
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
|   |-- ...
|-- manage.py
|-- .gitignore
|-- README.md
|-- ...
```
## Cómo Contribuir

¡Estoy abierto a contribuciones! Si deseas participar, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea un entorno virtual.
    ```bash
    python -m venv venv
    ```

3. Activa el entorno virtual.
   - En Windows: `.\\venv\\Scripts\\activate`
   - En macOS/Linux: `source venv/bin/activate`

4. Instala las dependencias.
    ```bash
    pip install -r requirements.txt
    ```

5. Para poder usar la página, deberás llenar la base de datos con al menos los animes que están en la lista de últimos episodios.

6. Crea la base de datos en MySQL. Asegúrate de ponerle utf-8 unicode.

7. Genera las migraciones.

8. Debes hacer algunas correcciones en la API. Encuéntralas aquí:
```
|-- animes/
|   |-- management/
|   |   |-- correciones api
|   |   |   |-- animeflv.py
```
9. Para importar la informacion de los animes, hay un script en:
```
|-- animes/
|   |-- management/
|   |   |-- import_anime_list.py
```
11. Cambia las claves de los animes que seran importados.
12. Crea una rama para tu nueva función: git checkout -b nombre-de-la-funcion.
13. Realiza tus cambios y asegúrate de seguir las mejores prácticas.
14. Haz commit de tus cambios: git commit -m "Añadida función: nombre-de-la-funcion".
15. Haz push a tu rama: git push origin nombre-de-la-funcion.
16. Abre un Pull Request y describe tus cambios.
## Contacto

¡Me encantaría saber tu opinión! Puedes contactarme a través de [ramonfelipeperezosorio@gmail.com](mailto:ramonfelipeperezosorio@gmail.com) o [mi perfil de LinkedIn](https://www.linkedin.com/in/ram%C3%B3n-felipe-perez-osorio).

¡Espero que disfrutes explorando la página de anime!
