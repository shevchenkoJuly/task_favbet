import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1. Завантаження оброблених даних з Excel:
data = pd.read_excel('data/processed/cleaned_user_data.xlsx')

money_threshold = data['Money'].median() 
lifetime_threshold = data['LifeTime'].median()
lastlog_threshold = 30

# 2. Створення нових колонок для категорій:
data['Payment_Category'] = data['Money'].apply(lambda x: 'High' if x > money_threshold else 'Low')
data['LifeTime_Category'] = data['LifeTime'].apply(lambda x: 'Loyal' if x > lifetime_threshold else 'New')
data['Activity_Category'] = data['LastLog'].apply(lambda x: 'Inactive' if x > lastlog_threshold  else 'Active')

# 3. Підготовка сегментів:
X = data[['Money', 'LifeTime', 'LastLog']]

# 4. Масштабування даних:
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Виконання  K-means - метод кластеризації
kmeans = KMeans(n_clusters=4, random_state=42)
data['Cluster'] = kmeans.fit_predict(X_scaled)

# 6. Створення підсумкової таблиці для опису кожного сегмента:
cluster_summary = data.groupby('Cluster').agg({
    'User_id': 'count',          # Кількість користувачів у кластері
    'Money': 'sum',              # Загальна сума витрат
    'LifeTime': 'mean',          # Середня тривалість життя клієнтів
    'LastLog': 'mean'            # Середній час останнього входу
}).reset_index()

# Перейменування колонок:
cluster_summary.columns = ['Cluster', 'Num_Users', 'Total_Money', 'Avg_LifeTime', 'Avg_LastLog']

# Обчислення часток по користувачах та монетизації:
total_users = data['User_id'].count()
total_money = data['Money'].sum()

cluster_summary['User_Share'] = (cluster_summary['Num_Users'] / total_users) * 100
cluster_summary['Money_Share'] = (cluster_summary['Total_Money'] / total_money) * 100

cluster_summary['User_Share'] = cluster_summary['User_Share'].round(2)
cluster_summary['Money_Share'] = cluster_summary['Money_Share'].round(2)
cluster_summary['Avg_LifeTime'] = cluster_summary['Avg_LifeTime'].round().astype(int)
cluster_summary['Avg_LastLog'] = cluster_summary['Avg_LastLog'].round().astype(int)

# 7. Сортування даних для збереження у вигляді групованої таблиці:
data_sorted = data.sort_values(by='Cluster')

# 8. Збереження відсортованих результатів:
data_sorted.to_excel('data/outputs/clustering_results_grouped.xlsx', index=False)

# 9. Збереження підсумкової таблиці по сегментах :
cluster_summary.to_excel('data/outputs/cluster_summary.xlsx', index=False)

