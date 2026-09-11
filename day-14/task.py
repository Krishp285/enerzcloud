import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

# Load example data
data = load_iris()
X = data.data
y = data.target

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print("Explained variance ratio:", pca.explained_variance_ratio_)

# Visualize
plt.figure(figsize=(8,6))
for label in np.unique(y):
    plt.scatter(X_pca[y==label, 0], X_pca[y==label, 1], label=data.target_names[label])
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA on Iris Dataset')
plt.legend()
plt.show()






# Load a dataset (e.g., Wine dataset).
from sklearn.datasets import Wine
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# Standardize features.

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA, plot explained variance ratio.
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print(X_pca)

# Visualize data projected onto first two PCs.
plt.figure(figsize=(8,6))
for label in np.unique(y):
    plt.scatter(X_pca[y==label, 0], X_pca[y==label, 1], label=data.target_names[label])
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA on Wine Dataset')
plt.legend()
plt.show()

# Try reconstructing original data from PCs and compute reconstruction error.

X_reconstructed = pca.inverse_transform(X_pca)
reconstruction_error = np.mean((X_scaled - X_reconstructed)**2)
print("Reconstruction error:", reconstruction_error)

# Explore effects of scaling and outliers on PCA results
