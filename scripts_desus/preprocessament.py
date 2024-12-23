"""
Script per preprocessader les dades de salut mental i contaminació de BCN --> En desús perquè primer volem codificar i 

Creat per: Lucía Revaliente i Aránzazu Miguélez

Data de creació: 08/12/24

Objectiu: L'objectiu d'aquest script és garantir que les dades s'ajustin de manera òptima 
a un model d'anàlisi o aprenentatge automàtic, evitant que certs tipus de dades prevalguin 
indegudament i permetent una comparació justa entre les diferents variables.

Descripció: Aquest script codifica les dades categòriques i numèriques:
                1. Categòriques nominals: OneHotEncoder
                2. Categòriques ordinals: StandardScaler
                3. Numèriques (ordinals i contínues)
"""
# IMPORTACIÓ
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd

# VARIABLES 
# Noms dels arxius pickle
DATASET_PATH = 'data/cleaned_dataset.pkl'
OUTPUT_PATH = 'data/preprocessed_data.pkl'  # Ruta donde se guardará el archivo pickle

#MAIN
# Carreguem pickle
data = pd.read_pickle(DATASET_PATH)

# Definir les columnes segons el tipus
num_cols = data.select_dtypes(include=['float64', 'int64']).columns  # Numèriques

ordinal_cols = {
    "education": ["primario o menos", "bachillerato", "universitario"],
    "covid_work": ["ha empeorado mucho", "ha empeorado un poco", "no ha cambiado", "ha mejorado un poco", "ha mejorado mucho"],
    "covid_mood": ["ha empeorado mucho", "ha empeorado un poco", "no ha cambiado", "ha mejorado un poco", "ha mejorado mucho"],  #"ha mejorado mucho" no está en el dataset
    "covid_sleep": ["ha empeorado mucho", "ha empeorado un poco", "no ha cambiado", "ha mejorado un poco", "ha mejorado mucho"], #"ha mejorado mucho" no está en el dataset
    "covid_espacios": ["le doy menos importancia que antes", "no ha cambiado", "le doy más importancia que antes"],  #"le doy menos importancia que antes" no está en el dataset
    "covid_aire": ["le doy menos importancia que antes", "no ha cambiado", "le doy más importancia que antes"],
    "covid_motor": ["lo utilizo menos que antes", "lo utilizo igual que antes", "lo utilizo más que antes"],
    "covid_electric": ["lo utilizo menos que antes", "lo utilizo igual que antes", "lo utilizo más que antes"],
    "covid_bikewalk": ["lo utilizo menos que antes", "lo utilizo igual que antes", "lo utilizo más que antes"],
    "covid_public_trans": ["lo utilizo menos que antes", "lo utilizo igual que antes", "lo utilizo más que antes"]
}  # Categòriques ordinals

nominal_cols = data.select_dtypes(include=['object']).columns.difference(ordinal_cols.keys())  # Categòriques nominals

# Crear transformadors específics per a cada tipus de variable
NUMERICAL_TRANSFORMER = StandardScaler()       # Escalar numèriques
ORDINAL_TRANSFORMER = OrdinalEncoder(categories=list(ordinal_cols.values()))  # Codificar ordinals
NOMINAL_TRANSFORMER = OneHotEncoder()          # Codificar nominals (one-hot)


# Configurar el ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', NUMERICAL_TRANSFORMER, num_cols),           # Escalar numèriques
        ('ord', ORDINAL_TRANSFORMER, list(ordinal_cols.keys())),         # Codificar ordinals
        ('nom', NOMINAL_TRANSFORMER, nominal_cols)          # Codificar nominals
    ]
)

# Crear pipeline complet
pipeline = Pipeline(steps=[('preprocessor', preprocessor)])

# Aplicar el pipeline al dataset
data_transformed = pipeline.fit_transform(data)

# Convertir el resultat a DataFrame
# Afegim noms de columnes per als one-hot encoding
encoded_nom_cols = pipeline.named_steps['preprocessor'].transformers_[2][1].get_feature_names_out(nominal_cols)
all_columns = list(num_cols) + list(ordinal_cols.keys()) + list(encoded_nom_cols)

# Crear DataFrame final
final_df = pd.DataFrame(data_transformed, columns=all_columns)
print(final_df)

# Guardem el pickle
final_df.to_pickle(OUTPUT_PATH)