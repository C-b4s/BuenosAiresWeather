#!/bin/bash

# FUENTE CONSULTADA:
# - Conda Env Scripting: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

# Cargar conda de forma segura usando bash desde $HOME
if [ -f ~/miniforge3/etc/profile.d/conda.sh ]; then
    source ~/miniforge3/etc/profile.d/conda.sh
elif [ -f ~/miniconda3/etc/profile.d/conda.sh ]; then
    source ~/miniconda3/etc/profile.d/conda.sh
elif [ -f ~/anaconda3/etc/profile.d/conda.sh ]; then
    source ~/anaconda3/etc/profile.d/conda.sh
fi

# Activar el entorno
conda activate iccd332

# Para que se mueva a la carpeta del proyecto para que crontab sepa dónde guardar los archivos
cd ~/BuenosAiresWeather

# Ejecutar el script de Python para Buenos Aires
python main.py
