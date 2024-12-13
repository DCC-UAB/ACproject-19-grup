from evaluation_regression import get_best_model
from preparation_regression import load_data, separacio_train_test
from preprocess import preprocess
from models_regression import RegressionModels, GRID_PARAMS, get_best_model
import pandas as pd
import os
from sklearn.feature_selection import SelectKBest, f_regression

# Configuración
DATA_PATH = "data/shuffled_scaled_dataset.pkl"
TARGET_COLUMN = "estres"

# Preparación de datos
def prepare_data(data, target_column):
    # data = preprocess(data_path, target_column)
    return separacio_train_test(data, target_column)

X_train, X_test, y_train, y_test = prepare_data(pd.read_pickle(DATA_PATH), TARGET_COLUMN)

# Evaluar modelos y calcular importancia de características
def evaluate_models(model_types, X_train, y_train):
     results = {}
     for model_name in model_types:
         print(f"Evaluando {model_name}...")
         model_instance = RegressionModels(model_type=model_name)
         param_grid = GRID_PARAMS.get(model_name, {})
         best_model = get_best_model(model_name, model_instance.get_model(), param_grid,X_train, y_train,X_test, y_test)
         best_model.fit(X_train, y_train)
         # Obtener importancia de características
         if hasattr(best_model, "coef_"):  # Modelos lineales
             coefficients = pd.DataFrame({
                 'Feature': X_train.columns,
                 'Coefficient': abs(best_model.coef_)
             }).sort_values(by='Coefficient', ascending=False)
             results[model_name] = coefficients

         elif hasattr(best_model, "feature_importances_"):  # Modelos de árboles
             importances = pd.DataFrame({
                 'Feature': X_train.columns,
                 'Importance': best_model.feature_importances_
             }).sort_values(by='Importance', ascending=False)
             results[model_name] = importances

         else:  # Modelos sin coeficientes directos
             from sklearn.inspection import permutation_importance
             perm_importance = permutation_importance(best_model, X_train, y_train, random_state=42)
             importances = pd.DataFrame({
                 'Feature': X_train.columns,
                 'Importance': perm_importance.importances_mean
             }).sort_values(by='Importance', ascending=False)
             results[model_name] = importances
     return results

# Guardar resultados
def save_results(results, output_dir="data/regression/results"):
    os.makedirs(output_dir, exist_ok=True)
    for model_name, importance_df in results.items():
        importance_df.to_excel(os.path.join(output_dir, f"{model_name}_importance.xlsx"), index=False)
        print(f"Resultados guardados para {model_name} en {output_dir}")

# # Extraer las 10 características más importantes comunes entre los métodos
# def extract_top_common_features(results, top_n=50):
#     """
#     Extrae las características comunes más importantes de los resultados.
    
#     Args:
#         results (dict): Diccionario con las importancias de las características por modelo.
#         top_n (int): Número de características principales a considerar de cada modelo.

#     Returns:
#         set: Conjunto de características comunes entre los modelos.
#     """
#     # Lista para almacenar conjuntos de las características más importantes
#     top_features_sets = []
    
#     for model_name, importance_df in results.items():
#         # Tomar las top_n características más importantes de cada modelo
#         top_features = set(importance_df.head(top_n)['Feature'])
#         top_features_sets.append(top_features)
    
#     # Intersección de las características principales de todos los modelos
#     common_features = set.intersection(*top_features_sets)
#     return common_features

def select_k_best_features(X_train, y_train, k):
    """
    Selecciona las k mejores características usando SelectKBest.
    """
    selector = SelectKBest(score_func=f_regression, k=k)
    X_train_selected = selector.fit_transform(X_train, y_train)
    selected_features = X_train.columns[selector.get_support()]
    return X_train_selected, selected_features, selector

# Ejecución principal
if __name__ == "__main__":
    model_types = [ "random_forest", "gradient_boosting", "xgboost"]
    results = evaluate_models(model_types, X_train, y_train)
    save_results(results)
    # print("Evaluación completada.")

    # Extraer las 10 características más importantes comunes
    common_features = select_k_best_features(X_train,y_train, 10)
    print("Las 10 características más importantes comunes entre los modelos son:")
    print(common_features)
    print("Evaluación completada.")
