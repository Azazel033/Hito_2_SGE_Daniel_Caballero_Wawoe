# Aplicación de Consulta de Base de Datos

Esta es una aplicación desarrollada en Python que permite interactuar con una base de datos MySQL para consultar, filtrar y analizar datos de manera visual. La aplicación incluye opciones para generar gráficos y exportar los resultados a un archivo Excel.

## Características

- **Inicio de sesión**: Conexión a una base de datos MySQL proporcionando usuario, contraseña y nombre de la base de datos.
- **Filtros personalizados**: Filtra los datos según criterios como edad, sexo, y diversos indicadores de salud y hábitos.
- **Resultados visuales**:
  - Visualización de los datos consultados en una tabla interactiva.
  - Ordenamiento de las columnas con un clic.
  - Exportación de resultados a un archivo Excel.
  - Generación de gráficos (barras, líneas, pastel) a partir de los datos consultados.
  
## Requisitos del sistema

- Python 3.8 o superior
- MySQL (debe estar configurado y accesible desde la máquina donde se ejecuta la aplicación)

### Librerías requeridas

Asegúrate de instalar las siguientes librerías antes de ejecutar la aplicación:

```bash
pip install tkinter pandas mysql-connector-python matplotlib openpyxl
