"""
Antes:
    1. Eliminar valores null, escalar los datos y seleccionar las variables.
    2. Determinar número óptimo de clusters
    3. Aplicar algoritmo de clústering
"""
# IMPORTACIÓ
import pandas as pd
from scipy.stats import shapiro

# VARIABLES CONSTANTS
PATH_DATASET = "data/cleaned_dataset.pkl"

# FUNCIONS
def estudiar_normalitat(df):
    # Aplicar Shapiro-Wilk a cada columna numérica
    resultados = {}
    for columna in df.select_dtypes(include=['float64', 'int64']).columns:  # Solo columnas numéricas
        stat, p_value = shapiro(df[columna].dropna())  # Ignora valores NaN
        resultados[columna] = {"Estadístico W": stat, "Valor p": p_value}

    # Mostrar resultados
    for columna, res in resultados.items():
        print(f"Columna: {columna}")
        print(f"  Estadístico W: {res['Estadístico W']:.4f}")
        print(f"  Valor p: {res['Valor p']:.4f}")
        if res["Valor p"] > 0.05:
            print("  → Los datos parecen seguir una distribución normal.")
        else:
            print("  → Los datos no siguen una distribución normal.")

# CLASSE
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class ClusteringModel:
    def __init__(self, data, n_clusters=3, algorithm='kmeans'):
        """
        Constructor de la classe per a modelar el clustering.
        
        :param data: DataFrame o ndarray amb les dades a clustering.
        :param n_clusters: Nombre de clusters a identificar. Per defecte 3.
        :param algorithm: Algoritme de clustering a utilitzar. Pot ser 'kmeans', 'spectral', 'agglo', 'gmm'.
        """
        self.data = data
        self.n_clusters = n_clusters
        self.algorithm = algorithm
        self.model = None
        self.labels = None

    def fit(self):
        """Entrenar el model segons l'algoritme seleccionat"""
        if self.algorithm == 'kmeans':
            self.model = KMeans(n_clusters=self.n_clusters)
        elif self.algorithm == 'spectral':
            self.model = SpectralClustering(n_clusters=self.n_clusters, affinity='nearest_neighbors')
        elif self.algorithm == 'agglo':
            self.model = AgglomerativeClustering(n_clusters=self.n_clusters)
        elif self.algorithm == 'gmm':
            self.model = GaussianMixture(n_components=self.n_clusters)
        else:
            raise ValueError(f'Algoritme {self.algorithm} no reconegut')
        
        # Ajustar el model a les dades
        self.model.fit(self.data)
        
        # Assignar les etiquetes (clusters) al conjunt de dades
        if self.algorithm == 'gmm':
            # En el cas de GaussianMixture, s'ha d'utilitzar predict per obtenir les etiquetes
            self.labels = self.model.predict(self.data)
        else:
            self.labels = self.model.labels_

    def silhouette_score(self):
        """Calcular la puntuació de silueta per mesurar la qualitat del clustering"""
        return silhouette_score(self.data, self.labels)

    def get_labels(self):
        """Obtenir les etiquetes de les prediccions"""
        return self.labels

    def set_clusters(self, n_clusters):
        """Establir el nombre de clusters"""
        self.n_clusters = n_clusters
        
    def set_algorithm(self, algorithm):
        """Establir l'algoritme de clustering"""
        self.algorithm = algorithm

    def evaluate(self):
        """Evaluar el model amb la puntuació de silueta"""
        score = self.silhouette_score()
        print(f"Puntuació de silueta per {self.algorithm}: {score}")
        return score
    
    def elbow_method(self, max_clusters=10):
        """
        Aplica el mètode del codo per trobar el millor nombre de clusters per KMeans.
        
        :param max_clusters: El màxim nombre de clusters a provar per al mètode del codo.
        """
        if self.algorithm != 'kmeans':
            raise ValueError("El mètode del codo només és aplicable per a KMeans.")
        
        inertia = []  # Llista per emmagatzemar les inèrcies per a cada nombre de clusters
        for n in range(1, max_clusters+1):
            kmeans = KMeans(n_clusters=n, random_state=42)
            kmeans.fit(self.data)
            inertia.append(kmeans.inertia_)
        
        # Dibuixar la gràfica per veure el "codo"
        plt.plot(range(1, max_clusters+1), inertia, marker='o')
        plt.title(f'Mètode del Colze. Sense reducció de var. max_clusters={max_clusters}')
        plt.xlabel('Nombre de clusters')
        plt.ylabel('Inèrcia')
        plt.show()

if __name__=="__main__":
    # 1 i 2. Codificació i escalat --> Carreguem les dades preprocessades
    df = pd.read_pickle("data/preprocessed_data.pkl")

    # 3. Sel·lecció de variables rellevants 
    # print(len(df.columns))

    # 4. El·lecció algoritme clustering: inicialitzar la classe ClusteringModel i provar els diferents algoritmes
    # clustering_kmeans = ClusteringModel(df, algorithm='kmeans')
    # clustering_kmeans.elbow_method(max_clusters=100)

    # clustering_kmeans = ClusteringModel(df, n_clusters=3, algorithm='kmeans')
    # clustering_kmeans.fit()
    # clustering_kmeans.evaluate()
    
    # clustering_spectral = ClusteringModel(df, n_clusters=3, algorithm='spectral')
    # clustering_spectral.fit()
    # clustering_spectral.evaluate()
    
    # clustering_agglo = ClusteringModel(df, n_clusters=3, algorithm='agglo')
    # clustering_agglo.fit()
    # clustering_agglo.evaluate()
    
    # clustering_gmm = ClusteringModel(df, n_clusters=3, algorithm='gmm')
    # clustering_gmm.fit()
    # clustering_gmm.evaluate()