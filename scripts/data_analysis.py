import pandas as pd

# Завантаження оброблених даних з Excel
data = pd.read_excel('data/processed/cleaned_user_data.xlsx')

# Розрахунок середнього віку
average_age = int(data['Year'].mean())
median_age = data['Year'].median()

# Визначення найпоширенішого віку
most_common_age = data['Year'].mode()[0]

summary_data = pd.DataFrame({
    'Statistic': ['Average Age', 'Median Age', 'Most Common Age'],
    'Value': [average_age, median_age, most_common_age]
})

# Визначення аномальних значень віку: 
Q1 = data['Year'].quantile(0.25)
Q3 = data['Year'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 2.5 * IQR 
upper_bound = Q3 + 2.5 * IQR 
outlier_age_IQR = data[(data['Year'] < lower_bound) | (data['Year'] > upper_bound) | (data['Year'] <= 1920)]

with pd.ExcelWriter('data/outputs/cleaned_user_data_with_statistics_and_outliers.xlsx') as writer:
    # Збереження основних статистик
    summary_data.to_excel(writer, sheet_name='Statistics', index=False)
    # Збереження аномальних значень
    outlier_age_IQR.to_excel(writer, sheet_name='Outlier Ages', index=False)

print(f"Середній вік: {average_age}")
print(f"Медіана віку: {median_age}")
print(f"Найпоширеніший вік: {most_common_age}")
print(f"Аномальні значення віку:\n{outlier_age_IQR}")
