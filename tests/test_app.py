# tests/test_app.py
import os
import sys

# Ajoute le dossier src au chemin de recherche Python
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)


def test_environment():
    """Vérifie simplement que l'environnement de test fonctionne."""
    assert True


def test_project_structure():
    """Vérifie que le fichier principal de l'application existe bien."""
    app_path = os.path.join(os.path.dirname(__file__), "../src/app.py")
    assert os.path.exists(app_path), "Le fichier src/app.py est introuvable !"