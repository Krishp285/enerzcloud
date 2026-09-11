# Mini Project: Exploratory Data Analysis (EDA)
# Dataset: Use either titanic or tips
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

titanic = pd.read_csv('day-7\Titanic-Dataset.csv')
print(titanic)

# Tasks:
# Show distribution of numerical features.
sns.histplot(titanic['Age'], kde=True)
plt.title('Distribution of Age')
plt.show()

# Visualize relationships between numeric variables (e.g., total_bill vs. tip).
sns.scatterplot(data=titanic, x='Age', y='Fare')
plt.title('Relationship between Age and Fare')
plt.show()

# Analyze categorical breakdowns using countplots and barplots.
sns.countplot(data=titanic, x='Pclass')
sns.barplot(data=titanic, x='Sex', y='Fare')
# Use at least 4 different Seaborn charts.
sns.boxplot(data=titanic, x='Pclass', y='Fare')
plt.title('Fare by Passenger Class')
plt.show()
sns.barplot(data=titanic, x='Sex', y='Fare')
plt.title('Fare by Sex')
plt.show()
sns.kdeplot(data=titanic['Fare'], shade=True)
plt.title('Kernel Density Estimate of Fare')
plt.show()
sns.violinplot(data=titanic, x='Sex', y='Fare')
plt.title('Fare by Sex')
plt.show()
# Make the final visualization presentable using themes and titles.
plt.title('Fare by Sex')
sns.set_theme(style='whitegrid')


# 6 visiualizations using  seaborn
sns.histplot(titanic['Age'], kde=True)
plt.title('Distribution of Age')
plt.show()
plt.savefig('distribution_of_age.png')
sns.violinplot(data=titanic, x='Sex', y='Fare')
plt.title('Fare by Sex')
plt.show()
plt.savefig('fare_by_sex.png')

sns.scatterplot(data=titanic, x='Age', y='Fare')
plt.title('Relationship between Age and Fare')
plt.show()
plt.savefig('age_vs_fare.png')
sns.lineplot(data=titanic, x='Pclass', y='Fare')
plt.title('Fare by Passenger Class')
plt.show()
plt.savefig('fare_by_passenger_class.png')             


sns.barplot(data=titanic, x='Sex', y='Fare')
plt.title('Fare by Sex')
plt.show()
plt.savefig('fare_by_sex_barplot.png')
sns.countplot(data=titanic, x='Pclass')
plt.title('Count of Passengers by Class')
plt.show()
plt.savefig('count_of_passengers_by_class.png')