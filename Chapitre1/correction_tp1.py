import nbformat
from nbconvert import PythonExporter
from nbconvert.preprocessors import ExecutePreprocessor

# Charger le notebook
notebook_filename = 'tp1.ipynb'
with open(notebook_filename) as f:
    nb = nbformat.read(f, as_version=4)

# Exécuter le notebook
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
ep.preprocess(nb, {'metadata': {'path': './'}})

# Convertir le notebook en script Python
python_exporter = PythonExporter()
python_code, _ = python_exporter.from_notebook_node(nb)

# Enregistrer le script Python dans un fichier temporaire
exec_globals = {}
exec(python_code, exec_globals)

# Tester la fonction somme
def test_somme():
    assert exec_globals['somme'](1, 2) == 3, "Test 1 échoué"
    assert exec_globals['somme'](5, 7) == 12, "Test 2 échoué"
    assert exec_globals['somme'](0, 0) == 0, "Test 3 échoué"
    print("Tous les tests ont réussi!")

# Lancer les tests
if __name__ == "__main__":
    test_somme()
