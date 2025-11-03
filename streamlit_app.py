import sys
import os

# Agregar la carpeta src al path para importar módulos internos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from visualizer import ejecutar_dashboard

if __name__ == "__main__":
    ejecutar_dashboard()