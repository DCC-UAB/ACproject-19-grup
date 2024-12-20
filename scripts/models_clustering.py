# IMPORTS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import SpectralClustering, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from matplotlib.animation import FuncAnimation
from sklearn.manifold import TSNE
import os

# CLASSE
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
            self.model = KMeans(n_clusters=self.n_clusters, random_state=42)
        elif self.algorithm == 'agglo':
            self.model = AgglomerativeClustering(n_clusters=self.n_clusters)
        elif self.algorithm == 'gmm':
            self.model = GaussianMixture(n_components=self.n_clusters, random_state=42)
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

    # CLUSTER SELECTION ------------------------------------------------------------------------------------
    def elbow_method(self, max_clusters=10):
        """
        Aplica el mètode del codo per trobar el millor nombre de clusters.
        """
        # Crear el model de clustering seguint l'algoritme seleccionat
        if self.algorithm == 'kmeans':
            model = KMeans(random_state=42)
        elif self.algorithm == 'agglo':
            model = AgglomerativeClustering()
        elif self.algorithm == 'gmm':
            model = GaussianMixture(random_state=42)
        else:
            raise ValueError(f"Algoritmo '{self.algorithm}' no és vàlid.")

        # Crear el visualitzador per veure el mètode del codo
        visualizer = KElbowVisualizer(model, k=(1, max_clusters))  # Provar entre 1 i max_clusters clusters

        # Ajustar el visualitzador a les dades escalades
        visualizer.fit(self.data)
        visualizer.show()

        # Obtenir el nombre òptim de clusters (el valor del codo)
        self.n_clusters = visualizer.elbow_value_
        print(f"El número òptim de clusters és: {self.n_clusters}")
        return visualizer.elbow_value_

    def gmm_best_k(self, max_clusters=10):
        """
        Encuentra el mejor número de clusters utilizando el BIC (Bayesian Information Criterion) en un GMM.
        
        :param max_clusters: Número máximo de clusters a evaluar (por defecto 10).
        :return: El número óptimo de clusters según el BIC.
        """
        bic_scores = []
        
        # Evaluar modelos GMM para cada número de clusters desde 1 hasta max_clusters
        for k in range(1, max_clusters + 1):
            gmm = GaussianMixture(n_components=k, random_state=42)
            gmm.fit(self.data)
            bic_scores.append(gmm.bic(self.data))  # Calcular el BIC para el modelo ajustado

        # Encontrar el número de clusters que minimiza el BIC
        best_k = np.argmin(bic_scores) + 1  # +1 porque el rango comienza en 1
        
        print(f"El número óptimo de clusters según el BIC es: {best_k}")
        self.n_clusters = best_k  # Establecer el número óptimo de clusters
        return best_k

    # VISUALIZATION -----------------------------------------------------------------------------
    def plot_clusters_PCA_2d(self):
        """
        Visualiza los datos en un gráfico 2D coloreados según el cluster.
        Utiliza PCA para reducir la dimensionalidad si hay más de 2 características.
        """
        if self.labels is None:
            raise ValueError("El modelo debe ser ajustado antes de graficar los clusters.")
        
        # Reducir a 2 dimensiones si es necesario
        if self.data.shape[1] > 2:
            pca = PCA(n_components=2)
            reduced_data = pca.fit_transform(self.data)
        else:
            reduced_data = self.data
        
        # Crear el scatter plot
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(
            reduced_data[:, 0], reduced_data[:, 1], 
            c=self.labels, cmap='viridis', s=50, alpha=0.6, edgecolor='k'
        )
        plt.title(f'Clusters Visualitzats ({self.algorithm}). PCA 2D.k={self.n_clusters}.')
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.colorbar(scatter, label='Cluster')
        plt.grid(True)
        plt.show()

    def plot_clusters_PCA_3d(self):
        """Visualitzar els clusters en un gràfic 3D"""
        # Si les dades tenen més de 3 dimensions, reduir a 3D amb PCA
        if self.data.shape[1] > 3:
            pca = PCA(n_components=3)
            reduced_data = pca.fit_transform(self.data)
        else:
            reduced_data = self.data

        # Crear el gràfic 3D amb els colors dels clusters
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        scatter = ax.scatter(
            reduced_data[:, 0], reduced_data[:, 1], reduced_data[:, 2],
            c=self.labels, cmap='viridis', s=50, alpha=0.8
        )
        ax.set_title(f'Clusters segons {self.algorithm}. PCA 3D.. k={self.n_clusters}.')
        ax.set_xlabel('Componente 1')
        ax.set_ylabel('Componente 2')
        ax.set_zlabel('Componente 3')
        fig.colorbar(scatter, label='Cluster')
        plt.show()
    
    def plot_clusters_TSNE_2d(self):
        """
        Visualiza los datos en un gráfico 2D coloreados según el cluster.
        Utiliza t-SNE para reducir la dimensionalidad si hay más de 2 características.
        """
        if self.labels is None:
            raise ValueError("El modelo debe ser ajustado antes de graficar los clusters.")
        
        # Reducir a 2 dimensiones si es necesario
        if self.data.shape[1] > 2:
            tsne = TSNE(n_components=2, random_state=42)
            reduced_data = tsne.fit_transform(self.data)
        else:
            reduced_data = self.data
        
        # Crear el scatter plot
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(
            reduced_data[:, 0], reduced_data[:, 1], 
            c=self.labels, cmap='viridis', s=50, alpha=0.6, edgecolor='k'
        )
        plt.title(f'Clusters Visualizados ({self.algorithm}). TSNE 2D. k={self.n_clusters}.')
        plt.xlabel('Componente 1')
        plt.ylabel('Componente 2')
        plt.colorbar(scatter, label='Cluster')
        plt.grid(True)
        plt.show()

    # import os
    # import numpy as np
    # import matplotlib.pyplot as plt
    # from mpl_toolkits.mplot3d import Axes3D
    # from sklearn.manifold import TSNE
    # import imageio

    # def plot_clusters_TSNE_3d(self, gif_filename="visualitzaciclusters_TSNE_3d.gif", frames=36):
    #     """
    #     Visualiza los datos en un gráfico 3D coloreados según el cluster.
    #     Utiliza t-SNE para reducir la dimensionalidad si hay más de 3 características.
    #     Guarda una animación en formato GIF rotando el gráfico.
        
    #     Parameters:
    #     - gif_filename: Nombre del archivo GIF que se guardará.
    #     - frames: Número de ángulos diferentes para la rotación.
    #     """
    #     if self.labels is None:
    #         raise ValueError("El modelo debe ser ajustado antes de graficar los clusters.")
        
    #     # Reducir a 3 dimensiones si es necesario
    #     if self.data.shape[1] > 3:
    #         tsne = TSNE(n_components=3, random_state=42)
    #         reduced_data = tsne.fit_transform(self.data)
    #     else:
    #         reduced_data = self.data
        
    #     # Crear el gráfico 3D
    #     fig = plt.figure(figsize=(10, 8))
    #     ax = fig.add_subplot(111, projection='3d')

    #     # Graficar los datos en 3D
    #     scatter = ax.scatter(
    #         reduced_data[:, 0], reduced_data[:, 1], reduced_data[:, 2],
    #         c=self.labels, cmap='viridis', s=50, alpha=0.6, edgecolor='k'
    #     )
    #     ax.set_title(f'Clusters Visualizados ({self.algorithm}). TSNE 3D. k={self.n_clusters}.')
    #     ax.set_xlabel('Componente 1')
    #     ax.set_ylabel('Componente 2')
    #     ax.set_zlabel('Componente 3')
    #     fig.colorbar(scatter, label='Cluster')

    #     # Guardar cada frame rotando el gráfico
    #     angles = np.linspace(0, 360, frames)  # Generar ángulos para rotación
    #     filenames = []

    #     for angle in angles:
    #         ax.view_init(elev=30, azim=angle)  # Rotar el gráfico
    #         temp_filename = f"frame_{int(angle)}.png"
    #         plt.savefig(temp_filename)  # Guardar cada frame como imagen
    #         filenames.append(temp_filename)

    #     plt.close()  # Cerrar el gráfico después de guardar los frames

    #     # Crear el GIF usando imageio
    #     with imageio.get_writer(gif_filename, mode='I', duration=0.1) as writer:
    #         for filename in filenames:
    #             image = imageio.imread(filename)
    #             writer.append_data(image)

    #     # Limpiar archivos temporales
    #     for filename in filenames:
    #         os.remove(filename)

    #     print(f"GIF guardado como {gif_filename}")

    #     return reduced_data


    def plot_clusters_TSNE_3d(self):
        """
        Visualiza los datos en un gráfico 3D coloreados según el cluster.
        Utiliza t-SNE para reducir la dimensionalidad si hay más de 3 características.
        """
        if self.labels is None:
            raise ValueError("El modelo debe ser ajustado antes de graficar los clusters.")
        
        # Reducir a 3 dimensiones si es necesario
        if self.data.shape[1] > 3:
            tsne = TSNE(n_components=3, random_state=42)
            reduced_data = tsne.fit_transform(self.data)
        else:
            reduced_data = self.data
        
        # Crear el gráfico 3D
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Graficar los datos en 3D
        scatter = ax.scatter(
            reduced_data[:, 0], reduced_data[:, 1], reduced_data[:, 2],
            c=self.labels, cmap='viridis', s=50, alpha=0.6, edgecolor='k'
        )
        ax.set_title(f'Clusters Visualizados ({self.algorithm}). TSNE 3D. k={self.n_clusters}.')
        ax.set_xlabel('Componente 1')
        ax.set_ylabel('Componente 2')
        ax.set_zlabel('Componente 3')
        fig.colorbar(scatter, label='Cluster')
        plt.show()

        return reduced_data

    def plot_clusters_TSNE_3d_animated(self, filename="clusters_3d.gif"):
        """
        Visualiza los datos en un gráfico 3D animado, coloreados según el cluster.
        Guarda la animación como un GIF.
        """
        if self.labels is None:
            raise ValueError("El modelo debe ser ajustado antes de graficar los clusters.")

        # Reducir a 3 dimensiones si es necesario
        if self.data.shape[1] > 3:
            tsne = TSNE(n_components=3, random_state=42)
            reduced_data = tsne.fit_transform(self.data)
        else:
            reduced_data = self.data

        # Crear el gráfico 3D
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Graficar los datos en 3D
        scatter = ax.scatter(
            reduced_data[:, 0], reduced_data[:, 1], reduced_data[:, 2],
            c=self.labels, cmap='viridis', s=50, alpha=0.6, edgecolor='k'
        )
        ax.set_title(f'Clusters Visualizados ({self.algorithm}). TSNE 3D. k={self.n_clusters}.')
        ax.set_xlabel('Componente 1')
        ax.set_ylabel('Componente 2')
        ax.set_zlabel('Componente 3')

        # Función para actualizar la animación (rotación del gráfico)
        def update(frame):
            ax.view_init(elev=30, azim=frame)
            return fig,

        # Crear animación
        ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50, blit=False)

        # Guardar como GIF
        ani.save(filename, writer='pillow', fps=20)
        plt.close(fig)
        print(f"Animación guardada como {filename}")

        return reduced_data


    # ANALYSIS OF CLUSTER CHARACTERISTICS -------------------------------------------------------------------------------------
    def analisi_components_centroides(self, preprocessed_df, k=5):
        """
        Analyze the most relevant features for each cluster based on the clustering algorithm.
        
        Parameters:
        - preprocessed_df: DataFrame with the original (non-reduced) features used for clustering.
        - k: Number of top/bottom features to analyze (default=5).
        
        Returns:
        - centroides_df: DataFrame with cluster centers or means per feature.
        - relevant_features: Dictionary mapping clusters to their top/bottom features.
        """
        if self.labels is None or self.model is None:
            raise ValueError("The model must be fitted before running this analysis.")

        if self.algorithm == 'kmeans':
            # KMeans: Direct access to centroids
            if not hasattr(self.model, 'cluster_centers_'):
                raise ValueError("KMeans model does not have centroids computed.")
            centroids = self.model.cluster_centers_

        elif self.algorithm == 'agglo':
            # AgglomerativeClustering: Compute feature averages per cluster
            clusters = pd.DataFrame(self.data, columns=preprocessed_df.columns)
            clusters['Cluster'] = self.labels
            centroids = clusters.groupby('Cluster').mean().values

        elif self.algorithm == 'gmm':
            # GaussianMixture: Use computed means
            if not hasattr(self.model, 'means_'):
                raise ValueError("GaussianMixture model does not have means computed.")
            centroids = self.model.means_

        else:
            raise ValueError("This function only supports 'kmeans', 'agglo', or 'gmm' algorithms.")

        # Convert centroids to DataFrame for better interpretation
        columns = preprocessed_df.columns  # Get feature names
        centroides_df = pd.DataFrame(centroids, columns=columns)
        centroides_df.index = [f"Cluster {i}" for i in range(len(centroides_df))]

        # Analyze top/bottom features for each cluster
        relevant_features = {}
        for cluster_idx, row in centroides_df.iterrows():
            # Top k features with highest/lowest centroid values
            top_features = row.nlargest(k).index.tolist()
            low_features = row.nsmallest(k).index.tolist()
            relevant_features[cluster_idx] = {
                'top': top_features,
                'low': low_features
            }

        return centroides_df, relevant_features

    def analisi_components_tsne_correlacio(self, reduced_data, k=5):
        """
        Realiza un análisis de correlación entre las características originales del conjunto de datos
        y las componentes obtenidas mediante reducción dimensional con t-SNE. Esta función calcula 
        las correlaciones entre cada componente de t-SNE y las variables originales, y devuelve una 
        lista de las k características con las correlaciones más fuertes (tanto positivas como negativas) 
        para cada componente.

        Parámetros:
        - reduced_data: ndarray o DataFrame que contiene los datos reducidos a través de t-SNE.
        Debe tener el mismo número de filas que self.data, y debe contener las componentes reducidas 
        generadas por t-SNE.
        - k: Número de correlaciones más fuertes (positivas y negativas) a identificar.

        Retorna:
        - correlations_df: DataFrame con las correlaciones completas.
        - dic_correlacions: un diccionario que contiene, para cada componente de t-SNE, las k variables 
        originales con las correlaciones más altas (positivas y negativas). La estructura es la siguiente:
        {
            'Component 1': {'top_positive': [var1, var2, ...], 'top_negative': [var3, var4, ...]},
            ...
        }
        """
        # Nombres de las componentes t-SNE
        COMPONENTS = [f"Component {i+1}" for i in range(reduced_data.shape[1])]

        # Convertir las coordenadas t-SNE a un DataFrame
        tsne_df = pd.DataFrame(reduced_data, columns=COMPONENTS)

        # Combinar datos originales con las componentes t-SNE
        combined_df = pd.concat([self.data, tsne_df], axis=1)

        # Calcular correlaciones completas entre variables originales y componentes t-SNE
        correlations = combined_df.corr().loc[self.data.columns, COMPONENTS]

        # Diccionario para guardar las correlaciones más significativas
        dic_correlacions = {}

        for comp in COMPONENTS:
            # Seleccionar las correlaciones de la componente actual
            correlacions = correlations[comp]

            # Obtener las k correlaciones más fuertes positivas y negativas
            top_k_positive = correlacions.sort_values(ascending=False).head(k)
            top_k_negative = correlacions.sort_values(ascending=True).head(k)

            # Almacenar en el diccionario
            dic_correlacions[comp] = {
                'top_positive': top_k_positive.index.tolist(),
                'top_negative': top_k_negative.index.tolist()
            }

        # Retornar el DataFrame completo y el diccionario de correlaciones
        return correlations, dic_correlacions

    # def analyze_target_distribution(self, original_df, target_col):
    #     """
    #     Analiza la distribución de la variable target dentro de cada cluster.

    #     :param original_df: DataFrame original que contiene la variable target.
    #     :param target_col: Nombre de la columna de la variable target en el DataFrame original.
    #     """
    #     if self.labels is None:
    #         raise ValueError("El modelo debe ser ajustado antes de analizar la distribución de la variable target.")
        
    #     # Crear un DataFrame con los clusters y la variable target
    #     analysis_df = pd.DataFrame({
    #         'Cluster': self.labels,
    #         target_col: original_df[target_col]
    #     })
        
    #     # Calcular la distribución de la variable target por cluster
    #     distribution = analysis_df.groupby('Cluster')[target_col].value_counts(normalize=True).unstack(fill_value=0)

    #     # Visualizar la distribución con un gráfico de barras
    #     distribution.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis', alpha=0.85)
    #     plt.title(f'Distribución de {target_col} por Cluster ({self.algorithm})')
    #     plt.xlabel('Cluster')
    #     plt.ylabel('Proporción')
    #     plt.legend(title=target_col, bbox_to_anchor=(1.05, 1), loc='upper left')
    #     plt.tight_layout()
    #     plt.show()

    #     return distribution

    def analyze_target_distribution(self, original_df, target_col, save_path=None):
        """
        Analiza la distribución de la variable target dentro de cada cluster y guarda el gráfico si se especifica una ruta.

        :param original_df: DataFrame original que contiene la variable target.
        :param target_col: Nombre de la columna de la variable target en el DataFrame original.
        :param save_path: Ruta donde se guardará el gráfico (opcional).
        """
        if self.labels is None:
            raise ValueError("El modelo debe ser ajustado antes de analizar la distribución de la variable target.")

        # Crear un DataFrame con los clusters y la variable target
        analysis_df = pd.DataFrame({
            'Cluster': self.labels,
            target_col: original_df[target_col]
        })

        # Calcular la distribución de la variable target por cluster
        distribution = analysis_df.groupby('Cluster')[target_col].value_counts(normalize=True).unstack(fill_value=0)

        # Visualizar la distribución con un gráfico de barras
        distribution.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis', alpha=0.85)
        plt.title(f'Distribución de {target_col} por Cluster ({self.algorithm})')
        plt.xlabel('Cluster')
        plt.ylabel('Proporción')
        plt.legend(title=target_col, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()

        # Guardar el gráfico si se proporciona una ruta
        if save_path:
            # Crear la carpeta si no existe
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path)
            print(f"Gráfico guardado en: {save_path}")

        plt.show()

        return distribution

if __name__=="__main__":
    import os

    

    # Imprimir la ruta resultante
    print(f"La ruta completa es: {target_path}")

    # Crear la carpeta si no existe
    os.makedirs(target_path, exist_ok=True)
