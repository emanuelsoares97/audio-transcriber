import os
import sys

# Garante que a raíz do projeto está no sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Opcional: muda diretório de trabalho para a raiz
os.chdir(PROJECT_ROOT)

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
