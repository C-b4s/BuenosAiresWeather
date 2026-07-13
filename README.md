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
```

## Control de errores

---

## 💻 1. En el Backend (Automatización y Servidor)

Aquí resolvemos el **`output.log`** en crudo y los mensajes para cuando se pruebe el script en la terminal del WSL.

### A. En el archivo `main.py` (Punto de entrada)

Se debe envolver la ejecución de todas las funciones del grupo en un único bloque `try-except` centralizado.

* **Qué agregar:**
```python
import logging
import sys

# Configurar el log para que SOLO guarde los errores en crudo
logging.basicConfig(filename='output.log', level=logging.ERROR, 
                    format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    # Mensaje amigable al usuario en consola
    print("[INFO] Iniciando adquisición de datos climatológicos...")

    try:
        # Aquí se ejecutan las funciones de los miembros del grupo
        # datos = obtener_clima_api()
        # guardar_en_csv(datos)

        # Mensaje amigable de éxito al usuario en consola
        print("✅ Datos guardados exitosamente en el CSV.")

    except Exception as e:
        # 1. Mensaje amigable para el usuario que está en la terminal:
        print("\n❌ Ocurrió un problema al ejecutar el script.")
        print("   La operación no pudo completarse. Por favor, revisa el archivo 'output.log'.")

        # 2. El requisito del log en CRUDO para el archivo:
        logging.exception("Excepción no controlada en el sistema:")
        sys.exit(1)

```



### B. En el comando de Crontab

La guía pide: *"Respalde la ejecución de crontab en un archivo output.log"*.

* **Qué agregar:** Al configurar el cron con `crontab -e`, agreguen la redirección de Linux al final del comando. Esto asegura que si el script de Bash (`.sh`) tiene un error de Linux, también se registre en crudo.
* **Dónde:** En el archivo de configuración de Cron de su usuario en WSL:
```bash
*/15 * * * * /ruta/exacta/get-weather.sh >> /ruta/exacta/output.log 2>&1

```



---

## 🌐 2. En el Frontend (Sitio Web en la carpeta `weather-site`)

Aquí es donde se manejan los mensajes de confirmación, advertencia y error **para el usuario que navega en la web**.

### A. En la Página 2: Lógica Matemática (`ieee754.org` / HTML / JS)

El usuario interactúa enviando números para convertirlos o sumarlos. Deben agregar elementos visuales controlados por JavaScript.

* **Qué agregar en el HTML (dentro del archivo `.org`):** Contenedores vacíos para los mensajes.
```html
<input type="text" id="numeroDecimal" placeholder="Ej. 15.25">
<button onclick="procesarIEEE()">Convertir</button>

<!-- Zona para mensajes al usuario -->
<div id="mensajeUsuario" style="margin-top: 10px; font-weight: bold;"></div>
<!-- Zona para el resultado exitoso -->
<div id="resultadoBits"></div>

```


* **Qué agregar en el JavaScript (Lógica Funcional):**
```javascript
const procesarIEEE = () => {
    const input = document.getElementById("numeroDecimal").value;
    const contenedorMensaje = document.getElementById("mensajeUsuario");
    const contenedorResultado = document.getElementById("resultadoBits");

    // Validación: Si no es un número (Advertencia al usuario)
    if (isNaN(input) || input.trim() === "") {
        contenedorMensaje.style.color = "orange";
        contenedorMensaje.innerText = "⚠️ Advertencia: Por favor, ingresa un número decimal válido.";
        contenedorResultado.innerText = "";
        return;
    }

    // Si todo está bien (Confirmación al usuario)
    // const resultado = convertir(parseFloat(input)); (Tu función pura)
    contenedorMensaje.style.color = "green";
    contenedorMensaje.innerText = "✅ Conversión realizada con éxito.";
    contenedorResultado.innerText = `Resultado en bits: 01000001011101...`;
};

```



### B. En la Página 3: Datos del INEC (`seguridad.org` / Python)

Como esta página procesa datos del INEC usando bloques de código de Python en Org-mode, se debe imprimir texto plano descriptivo sobre cómo se procesaron los datos.

* **Qué agregar:** Bloques de texto explicativos antes de las tablas y gráficos.
```text
* Análisis de Cifras de Seguridad del INEC

Procesamiento de datos: Se descargaron las cifras oficiales del INEC. 
Se aplicó un filtro para remover registros nulos y se agruparon las 
frecuencias por provincias de la siguiente manera:

#+BEGIN_SRC python :exports results :results value table
# Código de Python puramente matemático que genera la tabla...
#+END_SRC

```



---

## 📋 Resumen del Check-list para el grupo

1. **`output.log`:** Se alimenta automáticamente por el comando de **Crontab** y el `logging.exception()` dentro de **`main.py`**.
2. **Mensajes amigables en consola:** Se manejan con `print()` en el `try-except` de **`main.py`**.
3. **Mensajes al usuario en la web (Advertencia/Confirmación):** Se manejan dinámicamente con modificaciones en las etiquetas `<div>` mediante **JavaScript** en la página de **IEEE 754**.
