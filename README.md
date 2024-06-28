# Proyecto de Integración de Bases de Datos con Docker y Python

Este proyecto integra dos bases de datos, MySQL y PostgreSQL, utilizando Docker y una aplicación Python para transferir datos entre ellas.

## Estructura del Proyecto

project-root/
│
├── config/
│ └── config.py
│
├── modules/
│ ├── mysql_module.py
│ └── postgres_module.py
│
├── wait-for-it.sh
├── schema_mysql.sql
├── schema.sql
├── app.py
├── Dockerfile
└── docker-compose.yml


### Archivos y Directorios

- `config/`: Contiene el archivo `config.py` con la configuración de las bases de datos.
- `modules/`: Contiene los módulos `mysql_module.py` y `postgres_module.py` para manejar las conexiones y operaciones con MySQL y PostgreSQL.
- `wait-for-it.sh`: Script que espera a que los servicios de bases de datos estén listos antes de ejecutar la aplicación.
- `schema_mysql.sql`: Script SQL para inicializar la base de datos MySQL.
- `schema.sql`: Script SQL para inicializar la base de datos PostgreSQL.
- `app.py`: Script principal de la aplicación Python.
- `Dockerfile`: Dockerfile para construir la imagen de la aplicación.
- `docker-compose.yml`: Archivo de configuración de Docker Compose para orquestar los servicios.


### Uso

Inicializar el Proyecto
Clonar el repositorio.

Asegúrate de tener Docker y Docker Compose instalados.

Ejecuta el siguiente comando para construir y levantar los servicios:
```console
docker-compose up --build
```
Verificar la Conexión y Transferencia de Datos
El contenedor app esperará a que mysql y postgres estén listos antes de ejecutar el script app.py, que transferirá los datos de PostgreSQL a MySQL.

### Notas
Asegúrate de que los scripts schema_mysql.sql y schema.sql están correctamente configurados para inicializar las bases de datos con las tablas necesarias.
Puedes modificar los archivos de configuración en el directorio config según tus necesidades.
¡Listo! Ahora tienes un proyecto de integración de bases de datos documentado y configurado para ejecutarse con Docker Compose.
