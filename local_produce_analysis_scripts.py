import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Fictive dataset string
data_str = """
UserID,VisitTimestamp,Source,PageViewed,ProductCategory,AddedToCart,PurchaseMade,PurchaseValue,UserFeedbackScore,FeedbackText
1,2024-04-07 10:05:00,Search,Homepage > Dairy,Dairy,Yes,Yes,25.50,4,Fast delivery!
2,2024-04-07 10:20:00,Social Media,Homepage > Fruits,Fruits,No,No,0.00,,N/A
3,2024-04-07 11:00:00,Direct,Homepage > Vegetables > Checkout,Vegetables,Yes,Yes,15.75,5,Loved the fresh veggies!
4,2024-04-07 11:30:00,Email,Homepage > Fruits > Dairy,Dairy,Yes,No,0.00,,N/A
5,2024-04-07 12:15:00,Search,Homepage > Vegetables,Vegetables,Yes,Yes,30.00,3,Some items were out of stock.
6,2024-04-07 12:45:00,Direct,Homepage > Fruits,Fruits,Yes,Yes,22.00,5,Great quality!
7,2024-04-07 13:10:00,Social Media,Homepage > Dairy,Dairy,No,No,0.00,,N/A
8,2024-04-07 13:45:00,Email,Homepage > Vegetables > Checkout,Vegetables,Yes,Yes,18.50,4,Very fresh.
9,2024-04-07 14:00:00,Search,Homepage > Dairy,Dairy,Yes,No,0.00,,N/A
10,2024-04-07 14:30:00,Social Media,Homepage > Fruits > Checkout,Fruits,Yes,Yes,20.00,4,Will buy again!
"""

# Load the data into a DataFrame
df = pd.read_csv(StringIO(data_str))

# Data Cleaning and Preparation
df['VisitTimestamp'] = pd.to_datetime(df['VisitTimestamp'])
df['AddedToCart'] = df['AddedToCart'] == 'Yes'
df['PurchaseMade'] = df['PurchaseMade'] == 'Yes'

# Analysis 1: Source Effectiveness
source_summary = df.groupby('Source').agg(
    Visitors=('UserID', 'nunique'),
    AddedToCart=('AddedToCart', 'sum'),
    Purchases=('PurchaseMade', 'sum'),
    TotalPurchaseValue=('PurchaseValue', 'sum')
).reset_index()
source_summary['CartAdditionRate'] = (source_summary['AddedToCart'] / source_summary['Visitors']) * 100
source_summary['PurchaseRate'] = (source_summary['Purchases'] / source_summary['Visitors']) * 100

# Analysis 2: Product Category Analysis
category_summary = df.groupby('ProductCategory').agg(
    Interactions=('UserID', 'count'),
    Purchases=('PurchaseMade', 'sum'),
    TotalPurchaseValue=('PurchaseValue', 'sum')
).reset_index()
category_summary['ConversionRate'] = (category_summary['Purchases'] / category_summary['Interactions']) * 100

# Analysis 3: Feedback Analysis
feedback_df = df.dropna(subset=['UserFeedbackScore'])
average_feedback_score = feedback_df['UserFeedbackScore'].mean()

# Visualization 1: Source Effectiveness
sns.set_style("whitegrid")
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.barplot(x='Source', y='PurchaseRate', data=source_summary, palette='coolwarm')
plt.title('Purchase Rate by Source')
plt.subplot(1, 2, 2)
sns.barplot(x='Source', y='TotalPurchaseValue', data=source_summary, palette='coolwarm')
plt.title('Total Purchase Value by Source')
plt.tight_layout()
plt.show()

# Visualization 2: Product Category Conversion Rate
plt.figure(figsize=(8, 6))
sns.barplot(x='ProductCategory', y='ConversionRate', data=category_summary, palette='viridis')
plt.title('Conversion Rate by Product Category')
plt.show()

# Visualization 3: User Feedback Score Distribution
plt.figure(figsize=(8, 6))
sns.histplot(feedback_df['UserFeedbackScore'], bins=5, kde=False, color='skyblue')
plt.title('Distribution of User Feedback Scores')
plt.xticks(range(1, 6))
plt.show()

# Visualization 4: Scatter Plot for Outliers
df['VisualFeedbackScore'] = df['UserFeedbackScore'].fillna(0)  # Temporary column for visualization
plt.figure(figsize=(10, 6))
sns.scatterplot(x='PurchaseValue', y='VisualFeedbackScore', data=df, hue='ProductCategory', style='PurchaseMade', s=100)
plt.title('Purchase Value vs. User Feedback Score by Product Category')
for index, row in df.iterrows():
    if row['PurchaseValue'] > 20 or row['UserFeedbackScore'] < 3:
        plt.text(row['PurchaseValue'] + 0.5, row['VisualFeedbackScore'], f"UserID {row['UserID']}")
plt.show()
