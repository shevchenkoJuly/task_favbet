import pandas as pd

# Завантаження даних
data = pd.read_excel('data/raw/users_data.xlsx', sheet_name='Sheet2')

# Перевірка пустих значень
print("Кількість пропущених значень до обробки даних:")
print(data.isnull().sum())

# Обробка даних
data = data.dropna(subset=['Year', 'Payments', 'Money', 'LifeTime'])  # Видалення пропущених значень
data['Year'] = data['Year'].astype(int)  
data['Money'] = data['Money'].astype(float) 
data['LifeTime'] = data['LifeTime'].astype(int) 
data['LastLog'] = data['LastLog'].astype(int)
data['LastPayment'] = data['LastPayment'].astype(int)

num_cols = data.select_dtypes(include=['int64', 'float64']).columns
for col in num_cols:
    data[col] = data[col].fillna(data[col].mean())

cat_cols = data.select_dtypes(include=['object']).columns
for col in cat_cols:
    data[col] = data[col].fillna(data[col].mode()[0])

print("Кількість пропущених значень після обробки:")
print(data.isnull().sum())

# Збереження даних
data.to_excel('data/processed/cleaned_user_data.xlsx', index=False)

