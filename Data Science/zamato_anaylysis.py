# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Visualization style
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Load datasets
zomato_df = pd.read_csv("zomato.csv", encoding='latin1')
country_df = pd.read_excel("Country-Code.xlsx")

# Merge datasets on 'Country Code'
merged_df = pd.merge(zomato_df, country_df, on='Country Code', how='left')

# Filter Indian data
india_df = merged_df[merged_df['Country'] == 'India']

# ----------------------------------------------
# 1. Top rated restaurants in each city in India
# ----------------------------------------------
top_rated = india_df[india_df['Aggregate rating'] >= 4.0]
top_rated = top_rated.sort_values(['City', 'Aggregate rating', 'Votes'], ascending=[True, False, False])
top_rated_restaurants = top_rated.groupby('City').head(1)

print("\nTop Rated Restaurants in Each Indian City:")
print(top_rated_restaurants[['City', 'Restaurant Name', 'Aggregate rating', 'Votes']])

# ----------------------------------------------
# 2. Relationship between Rating and Votes
# ----------------------------------------------
sns.scatterplot(data=india_df, x='Aggregate rating', y='Votes')
plt.title("Relationship between Rating and Votes (India)")
plt.xlabel("Aggregate Rating")
plt.ylabel("Votes")
plt.tight_layout()
plt.show()

# ----------------------------------------------
# 3. Number of Restaurants in Each Country
# ----------------------------------------------
restaurant_counts = merged_df['Country'].value_counts()

print("\nNumber of Restaurants in Each Country:")
for country, count in restaurant_counts.items():
    print(f"{country:<20} : {count}")

# ----------------------------------------------
# 4. Top 5 Restaurants with Online Delivery
# ----------------------------------------------
online_delivery = merged_df[merged_df['Has Online delivery'] == 'Yes']
top_5_online = online_delivery.sort_values(['Aggregate rating', 'Votes'], ascending=False).head(5)

print("\nTop 5 Restaurants with Online Delivery:")
print(top_5_online[['Restaurant Name', 'City', 'Aggregate rating', 'Votes']])

# ----------------------------------------------
# 5. Cheap but Best Restaurant in Each City (India)
# ----------------------------------------------
cheap_best = india_df[india_df['Aggregate rating'] > 0].copy()
cheap_best_sorted = cheap_best.sort_values(['City', 'Aggregate rating', 'Average Cost for two', 'Votes'], ascending=[True, False, True, False])
best_cheap_by_city = cheap_best_sorted.groupby('City').head(1)

print("\nCheap but Best Restaurant in Each Indian City:")
print(best_cheap_by_city[['City', 'Restaurant Name', 'Average Cost for two', 'Aggregate rating', 'Votes']])

# ----------------------------------------------
# 6. Top Cuisines in Each Country
# ----------------------------------------------
cuisine_by_country = defaultdict(lambda: defaultdict(int))
for _, row in merged_df.iterrows():
    country = row['Country']
    cuisines = str(row['Cuisines']).split(',') if pd.notnull(row['Cuisines']) else []
    for cuisine in cuisines:
        cuisine_by_country[country][cuisine.strip()] += 1

print("\nTop Cuisines in Each Country:")
for country, cuisines in cuisine_by_country.items():
    top_cuisines = sorted(cuisines.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"{country:<20} : {[c[0] for c in top_cuisines]}")

    # ----------------------------------------------
# 7. Aggregate Rating of All Restaurants in Each City
# ----------------------------------------------
agg_rating_per_city = merged_df.groupby(['Country', 'City'])['Aggregate rating'].mean().reset_index()

print("\nAverage Aggregate Rating per City in Each Country:")
print(agg_rating_per_city.head(10))  # Show top 10 for brevity

# ----------------------------------------------
# 8. Does Rating Influence Cost? (Box Plot)
# ----------------------------------------------
sns.boxplot(data=india_df[india_df['Average Cost for two'] < 3000], 
            x='Aggregate rating', y='Average Cost for two')
plt.title("Does Rating Influence Cost?")
plt.tight_layout()
plt.show()

# ----------------------------------------------
# 9. Top City by Restaurant Percentage (Pie Chart)
# ----------------------------------------------
city_counts = india_df['City'].value_counts()
top_cities = city_counts.head(5)
plt.pie(top_cities, labels=top_cities.index, autopct='%1.1f%%', startangle=140)
plt.title("Top 5 Cities by Restaurant Share (India)")
plt.axis('equal')
plt.tight_layout()
plt.show()

# ----------------------------------------------
# 10. Top Cuisines in Indian Restaurants (Pie Chart)
# ----------------------------------------------
cuisine_counter = defaultdict(int)
for cuisines in india_df['Cuisines'].dropna():
    for cuisine in cuisines.split(','):
        cuisine_counter[cuisine.strip()] += 1

# Top 5 cuisines
top_cuisines_india = sorted(cuisine_counter.items(), key=lambda x: x[1], reverse=True)[:5]
labels, sizes = zip(*top_cuisines_india)
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title("Top Cuisines in Indian Restaurants")
plt.axis('equal')
plt.tight_layout()
plt.show()

