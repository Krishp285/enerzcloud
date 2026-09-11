import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.metrics import silhouette_score

# Load a dataset (e.g., Iris dataset).
iris = load_iris()
X = iris.data
y = iris.target

# Perform hierarchical clustering using different linkage methods.
linkage_methods = ['ward', 'complete', 'average', 'single']
plt.figure(figsize=(15, 10))

for i, method in enumerate(linkage_methods):
    plt.subplot(2, 2, i+1)
    Z = linkage(X, method=method)
    dendrogram(Z)
    plt.title(f'Dendrogram - {method} linkage')

plt.tight_layout()
plt.show()

# Assign cluster labels and visualize clusters.
linkage_methods = ['ward', 'complete', 'average', 'single']
for i, method in enumerate(linkage_methods):
    Z = linkage(X, method=method)
    clusters = fcluster(Z, 3, criterion='maxclust')
    plt.figure(figsize=(8, 6))
    sns.scatterplot(X[:, 0], X[:, 1], hue=clusters, palette='viridis')
    plt.title(f'Clusters - {method} linkage')
    plt.xlabel('Sepal length')
    plt.ylabel('Sepal width')
    plt.show()

# Compare results using silhouette score.
silhouettes = {}
for i, method in enumerate(linkage_methods):
    Z = linkage(X, method=method)
    clusters = fcluster(Z, 3, criterion='maxclust')
    silhouettes[method] = silhouette_score(X, clusters)
print(silhouettes)

# Summarize findings and impact of linkage choices.
print("\nImpact of Linkage Choices:")
for method, score in silhouettes.items():
    print(f"{method} linkage: Silhouette Score = {score:.2f}")  