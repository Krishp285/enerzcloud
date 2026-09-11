# simple kmeans clustering example

import pandas as pd 
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler    
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#loading the dataset 
df = pd.read_csv("C:\\Users\\DELL\\OneDrive\\Desktop\\enerzcloud\\day-11\\Mall_Customers.csv")
df = df.drop(['CustomerID'],axis=1 )
df['Genre'] = df['Genre'].map({'Male':1 , 'Female':0})
print(df.head())

model = KMeans(n_clusters=3,random_state=42)
model.fit(df)
print(model.labels_)
print(model.cluster_centers_)
print(silhouette_score(df,model.labels_))
plt.scatter(df['Annual Income (k$)'],df['Spending Score (1-100)'],c=model.labels_)
plt.show()

model = KMeans(n_clusters=5,random_state=42)
model.fit(df)
print(model.labels_)
print(model.cluster_centers_)
print(silhouette_score(df,model.labels_))
plt.scatter(df['Annual Income (k$)'],df['Spending Score (1-100)'],c=model.labels_)
plt.show()

# elbow method  

scores = []

for k in range(2,10):
    model = KMeans(n_clusters=k,random_state=42)
    model.fit(df)
    scores.append(silhouette_score(df,model.labels_))



plt.plot(range(2,10),scores)
plt.show()
