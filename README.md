# Proyecto de Registro Climatológico y Análisis de Datos

Este repositorio contiene el proyecto grupal para el registro climatológico, procesamiento matemático (IEEE 754) y análisis estadístico (INEC). 

Para que el proyecto tenga una arquitectura limpia, estructurada y fácil de mantener, vamos a desarrollar el código utilizando principalmente el **Paradigma Funcional**. Esto nos ayudará a evitar errores de lógica y a que todo encaje perfectamente al integrar las páginas en Emacs.

---

## Reglas de Oro del Paradigma Funcional

Para que el código mantenga esta línea, intentemos aplicar estos tres pilares en la medida de lo posible:

1. **Evitar modificar variables (Inmutabilidad):** Una vez que definas una variable, diccionario o array, intenta no cambiar su valor original. Si necesitas modificar un dato, es mejor crear una copia nueva con el cambio.
2. **Funciones Puras:** Diseña tus funciones para que dependan *únicamente* de los argumentos que reciben. No deben modificar variables globales ni depender de estados externos.
3. **¿Qué pasa con los bucles (`for` y `while`)?:** Podemos usarlos, especialmente para recorrer listas o leer archivos de forma sencilla. La única regla al usarlos es **no modificar variables que estén fuera del bucle** para evitar efectos secundarios inesperados.

---

## 🛠️ Organización del Código por Componentes

Para trabajar de forma organizada y no pisarnos el código, nos dividiremos los requisitos técnicos de la siguiente manera:

### 1. Ingesta de Datos y API (Python)
* **Misión:** Conectar con OpenWeatherMap y guardar los datos en `clima-<ciudad>-hoy.csv` cada 15 minutos mediante `crontab`.
* **Enfoque Funcional:** Al recibir el JSON de la API, procesa los datos de forma segura. Utiliza `.get("rain", 0.0)` para manejar los campos opcionales de lluvia o nieve sin necesidad de usar condicionales complejos que rompan el flujo de datos.

### 2. Lógica Matemática - IEEE 754 (Python)
* **Misión:** Desarrollar la conversión u operaciones con punto flotante asignadas para la segunda página.
* **Enfoque Funcional:** Crea funciones matemáticas puras. Por ejemplo, una función `convertir_a_binario(numero)` debe recibir el dato, procesarlo y retornar la cadena de bits, sin guardar historiales ni alterar estados del programa.

### 3. Análisis de Datos - INEC (Python)
* **Misión:** Procesar las cifras de seguridad del INEC, generar la tabla y el gráfico estadístico para la tercera página.
* **Enfoque Funcional:** Al limpiar o filtrar los datos del INEC, genera nuevas colecciones de datos en lugar de modificar el set de datos original. Pasa los datos limpios directamente a las funciones de graficado.

### 4. Integración Web e Interactividad (HTML / JavaScript)
* **Misión:** Crear la estructura en carpetas, configurar `simple-httpd` en Emacs y añadir interactividad en el navegador con JS.
* **Enfoque Funcional en JS:** Prioriza el uso de `const` sobre `let`. Al manipular datos en el navegador para mostrarlos en las tablas, prefiere métodos nativos como `.map()` o `.filter()` que procesan la información de manera limpia y declarativa.

---

## 💡 Ejemplo Práctico: ¿Cómo escribir el código?

Cuando procesemos listas (como los 50 datos del clima), intentemos estructurarlo priorizando funciones que transformen los datos directamente:

```python
# Enfoque recomendado: Modular y sin alterar datos externos
def procesar_registro(registro):
    return {
        "temperatura": registro.get("main", {}).get("temp"),
        "lluvia": registro.get("rain", 0.0)
    }

# Podemos usar un for para construir la nueva lista de forma limpia
datos_limpios = []
for item in lista_api:
    datos_limpios.append(procesar_registro(item))
