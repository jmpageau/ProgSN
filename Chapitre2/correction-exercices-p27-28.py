import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from datetime import datetime
import math
import os
import pandas as pd

# Chemin vers le dossier contenant les sous-dossiers des étudiants
base_path = './Exercices-p27-28'  # Chemin de base où sont situés les dossiers des étudiants

# Initialisation de la liste des résultats
results = []

# Liste des résultats attendus
expected_results = [
    26 * 13,                                    #1
    datetime.now().year - 1985,                 #2
    2 * 3.1416 * 4,                             #3
    3.1416 * (8 / 2)**2,                        #4
    57.35 * 0.10,                               #5             
    57.35 * 0.15,                               #6 
    57.35 * 0.20,                               #7 
    118.92 + (118.92*0.05) + (118.92*.09975),   #8
    -4.9 * 4**2 + 10 * 4 + 50,                  #9
    math.sqrt(3**2 + 4**2),                     #10
    math.sqrt(8**2 - 5**2),                     #11
    (4/3) * 3.1416 * 3**3,                      #12
    ((-2)**2 - 2) / (3 * (3 * (-2) + 2)**2),    #13
    (7**3)**(1/3) - 7,                          #14
    100 * ((7**3)**(1/3) - 7)/7,                #15
    0.9,                                        #16
    0.9-(1 / (1 + 1/9)),                        #17
    100 * ((1 / (1 + 1/9)) - 0.9)/0.9           #18
    # Ajoutez ici les autres résultats attendus pour les autres énoncés
]

# Fonction pour comparer les résultats
def check_result(cell_output, expected):
    try:
        # Récupère la sortie de la cellule
        result = eval(cell_output.strip())
        return result == expected
    except:
        return False

# Parcourir les dossiers des étudiants
for student_folder in os.listdir(base_path):
    student_path = os.path.join(base_path, student_folder)
    if os.path.isdir(student_path):
        notebook_filename = os.path.join(student_path, 'Chapitre2-exercices-p27-28.ipynb')
        
        # Charger le notebook
        with open(notebook_filename, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        # Exécuter le notebook pour s'assurer que toutes les cellules sont calculées
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': student_path}})

        # Récupérer les résultats des cellules
        cells = nb.cells
        
        # Vérifier les réponses et calculer la note
        correct_answers = 0
        total_exercises = len(expected_results)
        failed_exercises = []  # Liste pour enregistrer les numéros des exercices échoués
        
        exercice = 0
        for i, cell in enumerate(cells):
            if cell.cell_type == 'code' and exercice < total_exercises:
                # Prendre en compte uniquement les cellules de code et vérifier
                if check_result(cell.outputs[0]['data']['text/plain'], expected_results[exercice]):
                    correct_answers += 1
                else:
                    failed_exercises.append(exercice + 1)  # Enregistrer le numéro de l'exercice échoué
                exercice += 1

        # Calculer la note (en pourcentage)
        score = (correct_answers / total_exercises) * 100
        results.append({
            'Étudiant': student_folder, 
            'Note (%)': score,
            'Exercices échoués': ", ".join(map(str, failed_exercises)) if failed_exercises else "Aucun"
        })

# Enregistrer les résultats dans un fichier Excel
df_results = pd.DataFrame(results)
df_results.to_excel('resultats_etudiants-p27-28.xlsx', index=False)

print("Correction terminée. Les résultats sont enregistrés dans 'resultats_etudiants-p27-28.xlsx'.")
