# Mini Project Ideas:
# Each trainee selects one of the datasets and performs visualizations:

# ✅ Dataset 1: Weather Data
# Line plot of temperature over days

# Bar chart for average rainfall per month

# Pie chart for weather types (Sunny, Rainy, Cloudy)

import matplotlib.pyplot as plt

temp = [ 20, 22, 25, 23, 21, 24, 26 ]
day = [ 1, 2, 3, 4, 5, 6, 7 ]

# line plot of temperature over days
plt.plot(day, temp,marker='o', color='orange')
plt.title('Temperature over Days')
plt.xlabel('Days')
plt.ylabel('Temperature (degree C)')
plt.show()
plt.savefig('temperature_over_days_line_plot.png')
# bar chart for average rainfall per month
avg_rainfall = [ 40, 10, 70, 30, 90, 100, 50 ]
month = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul' ]
plt.bar(month, avg_rainfall, color='blue')
plt.title('Average Rainfall per Month')
plt.xlabel('Months')
plt.ylabel('Rainfall (mm)')
plt.show()
plt.savefig('average_rainfall_bar_chart.png')
# pie chart for weather types
labels = [ 'Sunny', 'Rainy', 'Cloudy' ]
size = [ 40, 30, 30 ]
plt.pie(size, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Weather Types')
plt.show()
plt.savefig('weather_types_pie_chart.png')
# scatter plot of temperature vs days
plt.scatter(day, temp, color='green')
plt.title('Temperature vs Days')
plt.xlabel('Days')
plt.ylabel('Temperature (degree C)')
plt.show()
plt.savefig('temperature_vs_days_scatter_plot.png')

