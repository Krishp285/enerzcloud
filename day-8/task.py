from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd

df = pd.read_csv('C:\\Users\\DELL\\OneDrive\\Desktop\\enerzcloud\\day-8\\Titanic-Dataset.csv')
print(df.head())

df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
df['Embarked'] = df['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
y = df['Survived']
x = df[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(x_train, y_train)
model_predictions = model.predict(x_test)
accuracy = accuracy_score(y_test, model_predictions)
print(f"Accuracy: {accuracy}") # 81