#!/bin/bash

# FUENTE CONSULTADA:
# - Conda Env Scripting: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html


# Cargar conda de forma segura usando bash desde mi usuario (martinpr)
if [ -f /home/martinpr/miniforge3/etc/profile.d/conda.sh ]; then
    source /home/martinpr/miniforge3/etc/profile.d/conda.sh
elif [ -f /home/martinpr/miniconda3/etc/profile.d/conda.sh ]; then
    source /home/martinpr/miniconda3/etc/profile.d/conda.sh
elif [ -f /home/martinpr/anaconda3/etc/profile.d/conda.sh ]; then
    source /home/martinpr/anaconda3/etc/profile.d/conda.sh
fi

# Activar el entorno
conda activate iccd332

# Para que se mueva a la carpeta del proyecto para que crontab sepa dónde guardar los archivos
cd /home/martinpr/BuenosAiresWeather

# Ejecutar el script de Python para Buenos Aires
python main.py
