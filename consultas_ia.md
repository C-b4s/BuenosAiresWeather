# Registro de Consultas a la IA - Martín Pérez

## 1. Problema de compatibilidad en entornos colaborativos (Rutas absolutas)
- Consulta: Cómo puedo evitar que el script falle al ejecutarse en las computadoras/máquinas de mis compañeros si tienen usuarios diferentes??
- Solución: Reemplazar las rutas absolutas estáticas por rutas relativas dinámicas usando "os.path.dirname(os.path.abspath(__file__))" en Python.

## 2. Error de Clave de API no autorizada (401 Unauthorized)
- Consulta: Por qué me da un error 401 con una API key nueva si la acabo de crear??
- Solución: Las claves nuevas de OpenWeatherMap toman hasta 2 horas en activarse. Se solucionó usando la API key del anterior Script que se usó para el clima de Quito.

## 3. Fallo en la activación del entorno Conda desde scripts (source: not found)
- Consulta: Al ejecutar el archivo .sh me da error con el comando source y no activa conda, cómo se le puede cambiar para que no me de este problema??
- Solución: Cambiar el intérprete del script de "/usr/bin/sh" a "/bin/bash" en la cabecera (shebang) ya que "sh" estándar no soporta la función "source" requerida para inicializar entornos virtuales de Conda de forma no interactiva.