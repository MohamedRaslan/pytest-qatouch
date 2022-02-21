!/bin/sh
#This script will create an env envirment if it dons't exist, insatll and update [pip wheel setuptools] and install all the nededed dependencies

ENV_DIR="env"
[ -d "${ENV_DIR}" ] &&  echo "Python Environment $ENV_DIR found." || echo "Python Environment $ENV_DIR not found."
[ ! -d "${ENV_DIR}" ] && python -m venv $ENV_DIR

./$ENV_DIR/Scripts/python -m ./$ENV_DIR/Scripts/pip install -U pip wheel setuptools
./$ENV_DIR/Scripts/pip install -e .[dev]
