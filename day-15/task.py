import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

# Load dataset
data = pd.read_csv('customer_data.csv')

# Feature selection
features = ['Age', 'Annual Income', 'Spending Score']
X = data[features]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determine k using elbow method
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.plot(range(1, 11), inertia, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()

# Choose k=4 for example
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

data['Cluster'] = clusters

# Silhouette score
score = silhouette_score(X_scaled, clusters)
print(f'Silhouette Score: {score:.2f}')