"""
Script per fer clustering amb diversos algoritmes i característiques.
Creat per: Lucía Revaliente i Aránzazu Miguélez
Data de creació: 12/12/24
Descripció: Aquest script carrega permet fer clustering amb diversos algoritmes i característiques
"""
# IMPORTACIÓ
from preprocess import preprocess
from models_clustering import ClusteringModel
import matplotlib.pyplot as plt
import os

# VARIABLES CONSTANTS
PATH_DATASET = "data/cleaned_dataset.pkl"  # Dataset netejat
ALGORITHMS = ['gmm']  # Algoritmes de clústering a provar: 'kmeans', 'agglo', 'gmm'
TARGET = 'estres'

current_path = os.getcwd() # Obtenir la ruta actual

# Dataset complet:
# VARIABLES_RELLEVANTS = []
# PATH_FILENAME = os.path.join(current_path, "visualizations", "clustering", "dataset")

# Les 9 variables noves més rellevants REGRESSIÓ:
# VARIABLES_RELLEVANTS = ['dayoftheweek', 'bienestar', 'energia', 'ordenador', 'alcohol', 'otrofactor', 'no2bcn_24h', 'no2gps_24h', 'covid_work']
# PATH_FILENAME = os.path.join(current_path, "visualizations", "clustering", "9th_important_features")

# Les 10 variables més rellevants XGBOOST:
# VARIABLES_RELLEVANTS = ['ordenador', 'otrofactor', 'dayoftheweek','district_gràcia','incidence_cat_physical incidence', 'smoke', 'district_sant andreu', 'bienestar', 'Totaltime']
# PATH_FILENAME = os.path.join(current_path, "visualizations", "clustering", "10th_important features")

# Les 4 variables més rellevants REGRESSIÓ i XGBOOST:
VARIABLES_RELLEVANTS = ['ordenador', 'otrofactor','dayoftheweek', 'bienestar']
PATH_FILENAME = os.path.join(current_path, "visualizations", "clustering", "4th_important_features")

# Agrupem les característiques mal balancejades: 
AGRUPATED = True  

# Per obtenir la k òptima:
ESCOLLIR_K = True
MAX_CLUSTERS = 50
COMPONENTS = ["Component 1", "Component 2", "Component 3"]

# VISUALITZACIONS:
VISUAL = 'TSNE'

# MAIN
if __name__=="__main__":
    # 1 i 2. Codificació i escalat
    whole_preprocessed_df = preprocess(PATH_DATASET, TARGET) # Carreguem les dades i les preprocessem
    
    if AGRUPATED: # Agrupar les classes 9 i 10 en una sola classe
        whole_preprocessed_df = whole_preprocessed_df.replace({10: 9})  # Canviar la classe 10 per la 9 en el conjunt d'entrenament

    preprocessed_df = whole_preprocessed_df.drop(TARGET, axis=1)  # Eliminem la variable a partir de la qual volem fer clústering

    # 3. Si hi ha variables rellevants, reduïm la dimensió del dataset
    if VARIABLES_RELLEVANTS: 
        preprocessed_df = preprocessed_df[VARIABLES_RELLEVANTS]  # Modifiquem el dataset

    # 4. Elecció de l'algoritme de clústering: Inicialitzem la classe i provem
    for algoritme in ALGORITHMS:
        # plt.ion()
        print(f'\nModel {algoritme}')
        model = ClusteringModel(data=preprocessed_df, algorithm=algoritme)
        
        if ESCOLLIR_K:
            if algoritme == 'gmm':
                best_k = model.gmm_best_k()
            else:
                best_k = model.elbow_method(max_clusters=MAX_CLUSTERS)
        else:
            # model.n_clusters=4
            model.n_clusters=5
            # model.n_clusters=6
            best_k = model.n_clusters
        
        print(f'Best number of clusters: {best_k}')
        model.fit()

        # Visualitzacions:
        if VISUAL == 'PCA':
            # model.plot_clusters_PCA_2d()
            model.plot_clusters_PCA_3d()
        else:
            # model.plot_clusters_TSNE_2d()
            # reduced_data = model.plot_clusters_TSNE_3d() 
            reduced_data = model.plot_clusters_TSNE_3d_animated(filename=f'{PATH_FILENAME}/aggrupated_8&9_{algoritme}_k{best_k}_TSNE3d_animated.gif')

        # Analitzar la distribució de la variable target
        print(f"Distribució de la variable target ('{TARGET}') per cluster:")
        target_distribution = model.analyze_target_distribution(whole_preprocessed_df, TARGET, save_path=f'{PATH_FILENAME}/aggrupated_8&9_{algoritme}_k{best_k}_distribution.png')
        print(target_distribution) 

        # Mostrar les característiques i els valors dels centroides per cada cluster
        centroides_df, caracteristiques_relevantes = model.analisi_components_centroides(preprocessed_df)

        print("Característiques segons centroides:")
        for cluster, data in caracteristiques_relevantes.items():
            print(f"\nCluster {cluster}:")
            print("  Variables més altes:")
            for feature in data['top']:
                # Imprimir el valor de cada característica en el centreide
                feature_value = centroides_df.loc[cluster, feature]
                print(f"    {feature}: {feature_value}")
            
            print("  Variables més baixes:")
            for feature in data['low']:
                # Imprimir el valor de cada característica en el centreide
                feature_value = centroides_df.loc[cluster, feature]
                print(f"    {feature}: {feature_value}")

        # Grups segons les correlacions de cada dimensió de TSNE: -------------------------------------------
        # correlations_df, dic_correlacions = model.analisi_components_tsne_correlacio(reduced_data, k=K)
        # print("Característiques segons components del TSNE:")
        # for comp, correlaciones in dic_correlacions.items():
        #     print(f"Component: {comp}")
        #     print(f"  Top positives: {correlaciones['top_positive']}")
        #     print(f"  Top negatives: {correlaciones['top_negative']}")

        # Grups segons els centroides ------------------------------------------------------------------------
        # centroides, caracteristiques_relevantes = model.analisi_components_centroides(preprocessed_df)
        # print("Característiques segons centroides:")
        # for cluster, data in caracteristiques_relevantes.items():
        #     print(f"Cluster {cluster}:")
        #     print(f"  Variables més altes: {data['top']}")
        #     print(f"  Variables més baixes: {data['low']}")
        # print()

if __name__ == '__main__':
    RESULTAT = {'CLUSTER 0': {'ordenador': 1, 'bienestar': 0.09},
                'CLUSTER 1': {'otrofactor': 1, 'dayoftheweek': 0.40},
                'CLUSTER 2': {'dayoftheweek': 1.47, 'bienestar': 0.47},
                'CLUSTER 3': {'ordenador': 1, 'otrofactor': 1},
                'CLUSTER 4': {'bienestar': 0.16}}
    
    # RESULTAT: 
    # Cluster Cluster 0:
    # Variables més altes:
    #     ordenador: 1.0
    #     bienestar: 0.09360505140624129
    #     dayoftheweek: -0.4085219179740924
    #     otrofactor: -1.0
    # Variables més baixes:
    #     otrofactor: -1.0
    #     dayoftheweek: -0.4085219179740924
    #     bienestar: 0.09360505140624129
    #     ordenador: 1.0

    # Cluster Cluster 1:
    # Variables més altes:
    #     otrofactor: 1.0
    #     dayoftheweek: 0.4019593168821394
    #     bienestar: -0.24698225039927516
    #     ordenador: -1.0
    # Variables més baixes:
    #     ordenador: -1.0
    #     bienestar: -0.24698225039927516
    #     dayoftheweek: 0.4019593168821394
    #     otrofactor: 1.0

    # Cluster Cluster 2:
    # Variables més altes:
    #     dayoftheweek: 1.4731547951186976
    #     bienestar: 0.472832262282025
    #     otrofactor: -1.0
    #     ordenador: -1.0
    # Variables més baixes:
    #     ordenador: -1.0
    #     otrofactor: -1.0
    #     bienestar: 0.472832262282025
    #     dayoftheweek: 1.4731547951186976

    # Cluster Cluster 3:
    # Variables més altes:
    #     ordenador: 1.0
    #     otrofactor: 1.0
    #     dayoftheweek: -0.38828883503761097
    #     bienestar: -0.5854100455473495
    # Variables més baixes:
    #     bienestar: -0.5854100455473495
    #     dayoftheweek: -0.38828883503761097
    #     otrofactor: 1.0
    #     ordenador: 1.0

    # Cluster Cluster 4:
    # Variables més altes:
    #     bienestar: 0.16137996374942615
    #     dayoftheweek: -0.014969355439394512
    #     otrofactor: -0.9999999999999992
    #     ordenador: -0.9999999999999992
    # Variables més baixes:
    #     ordenador: -0.9999999999999992
    #     otrofactor: -0.9999999999999992
    #     dayoftheweek: -0.014969355439394512
    #     bienestar: 0.16137996374942615
