from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import pandas as pd
CLEANED_DATASET_PATH = 'data\cleaned_dataset.pkl'

def codificar_columnas(dataset):
    """
    Codifica las columnas categóricas:
    - OrdinalEncoder para columnas ordinales.
    - OneHotEncoder para columnas nominales.

    Args:
        dataset (DataFrame): Dataset con columnas categóricas y numéricas.

    Returns:
        DataFrame: Dataset con columnas categóricas codificadas.
    """
    # Definir las columnas ordinales y sus órdenes
    ordinal_columns = {
    "education": ["primario o menos", "bachillerato", "universitario"],
    "covid_work": ["ha empeorado mucho", "ha empeorado un poco", "no ha cambiado", "ha mejorado un poco", "ha mejorado mucho"],
    "covid_mood": ["ha empeorado mucho", "ha empeorado un poco", "no ha cambiado", "ha mejorado un poco", "ha mejorado mucho"],
    "covid_sleep": ["ha empeorado mucho", "ha empeorado un poco", "no ha cambiado", "ha mejorado un poco", "ha mejorado mucho"],
    "covid_espacios": ["le doy menos importancia que antes", "no ha cambiado", "le doy más importancia que antes"],
    "covid_aire": ["le doy menos importancia que antes", "no ha cambiado", "le doy más importancia que antes"],
    "covid_motor": ["lo utilizo menos que antes", "lo utilizo igual que antes", "lo utilizo más que antes"],
    "covid_electric": ["lo utilizo menos que antes", "lo utilizo igual que antes", "lo utilizo más que antes"],
    "covid_bikewalk": ["lo utilizo menos que antes", "lo utilizo igual que antes", "lo utilizo más que antes"],
    "covid_public_trans": ["lo utilizo menos que antes", "lo utilizo igual que antes", "lo utilizo más que antes"]
}


    # Manejar valores faltantes en columnas ordinales
    # for col in ordinal_columns.keys():
    #     dataset[col] = dataset[col].fillna("Desconocido")
    #     if "Desconocido" not in ordinal_columns[col]:
    #         ordinal_columns[col].append("Desconocido")

    # Separar columnas nominales
    nominal_columns = dataset.select_dtypes(include=['object']).columns.difference(ordinal_columns.keys())

    # Codificar las columnas ordinales
    if ordinal_columns:
        print(f"Codificando columnas ordinales: {list(ordinal_columns.keys())}")
        ordinal_encoder = OrdinalEncoder(categories=list(ordinal_columns.values()))
        dataset[list(ordinal_columns.keys())] = ordinal_encoder.fit_transform(dataset[list(ordinal_columns.keys())])

    # Codificar las columnas nominales
    if len(nominal_columns) > 0:
        print(f"Codificando columnas nominales: {list(nominal_columns)}")
        nominal_encoder = OneHotEncoder(sparse_output=False)
        encoded_nominals = nominal_encoder.fit_transform(dataset[nominal_columns])

        # Convertir a DataFrame y concatenar con las columnas restantes
        encoded_df = pd.DataFrame(
            encoded_nominals,
            columns=nominal_encoder.get_feature_names_out(nominal_columns),
            index=dataset.index
        )
        dataset = pd.concat([dataset.drop(columns=nominal_columns), encoded_df], axis=1)

    return dataset

# Cargar el dataset
dataset_path = CLEANED_DATASET_PATH
data = pd.read_pickle(dataset_path)

# Aplicar codificación
dataset_codificado = codificar_columnas(data)

# Guardar el resultado
dataset_codificado.to_pickle('data/codif_dataset.pkl')
dataset_codificado.to_excel('data/codif_dataset.xlsx', index=False)
print("Dataset codificado guardado.")
