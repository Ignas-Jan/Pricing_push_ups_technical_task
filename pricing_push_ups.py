import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Reading of the dataset, check of shape and data
pricing_data_df = pd.read_csv("Vinted_technical_task/pricing_data.csv")

print(pricing_data_df.shape[0])
print("-" * 150)
print(pricing_data_df.info())
print("-" * 150)

push_up_price = 2 #setting the variable for push-up price
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Continuous and categorical columns recognition, analysis of different metrics
continuous_columns = pricing_data_df.select_dtypes(include=["int64", "float64"]).columns
categorical_columns = pricing_data_df.select_dtypes(include=["object"]).columns.tolist()

continuous_df = pd.DataFrame({
    "Feature": continuous_columns,
    "Count": [pricing_data_df[column].count() for column in continuous_columns],
    "% Miss": ["{:.2f}%".format(pricing_data_df[column].isnull().mean() * 100) for column in continuous_columns],
    "Card.": [pricing_data_df[column].nunique() for column in continuous_columns],
    "Min": [pricing_data_df[column].min() for column in continuous_columns],
    "Q1": ["{:.2f}".format(pricing_data_df[column].quantile(0.25)) for column in continuous_columns],
    "Mean": ["{:.2f}".format(pricing_data_df[column].mean()) for column in continuous_columns],
    "Median": ["{:.2f}".format(pricing_data_df[column].median()) for column in continuous_columns],
    "Q3": ["{:.2f}".format(pricing_data_df[column].quantile(0.75)) for column in continuous_columns],
    "Max": ["{:.2f}".format(pricing_data_df[column].max()) for column in continuous_columns],
    "Std. Dev.": ["{:.2f}".format(pricing_data_df[column].std()) for column in continuous_columns]
})
0
categorical_df = pd.DataFrame({
    "Feature": categorical_columns,
    "Count": [pricing_data_df[column].count() for column in categorical_columns],
    "% Miss": ["{:.2f}%".format(pricing_data_df[column].isnull().mean() * 100) for column in categorical_columns],
    "Card.": [pricing_data_df[column].nunique() for column in categorical_columns],
    "Mode": [pricing_data_df[column].mode()[0] for column in categorical_columns],
    "Mode Freq": [pricing_data_df[column].value_counts().iloc[0] for column in categorical_columns],
    "Mode %": ["{:.2f}%".format(pricing_data_df[column].value_counts(normalize=True).iloc[0] * 100) for column in categorical_columns],
    "2nd Mode": [pricing_data_df[column].value_counts().index[1] for column in categorical_columns],
    "2nd Mode Freq": [pricing_data_df[column].value_counts().iloc[1] for column in categorical_columns],
    "2nd Mode %": ["{:.2f}%".format(pricing_data_df[column].value_counts(normalize=True).iloc[1] * 100) for column in categorical_columns]
})

print(continuous_df)
print("-" * 150)
print(categorical_df)
print("-" * 150)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Checking the dataset for duplicated rows and handling it
duplicates = pricing_data_df[pricing_data_df.duplicated()]
print(f"{duplicates}")
print("-" * 150)
pricing_data_df = pricing_data_df.drop_duplicates()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Checking the dataset for negative values
negative_values = (pricing_data_df[["number_of_listings", "avg_listing_price_eur", "revenue_from_push_ups"]] < 0).any().reset_index()
negative_values.columns = ["Column", "Negative"]
print("-" * 150)
print(negative_values)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Checking the dataset for NULL values and their handling
miss_percentage = pd.DataFrame({
    "Count": pricing_data_df.isna().sum(),
    "Miss %": [f"{x:.2f}%" for x in pricing_data_df.isnull().mean() * 100]
})
print(miss_percentage)
print("-" * 150)

#Calculating the weight of NULL valued categories 2 and 3 on the dataset and how to handle it
unknown_data = pricing_data_df[pricing_data_df["category_3"].isnull()]
print(f"Unknown categories revenue: {unknown_data["revenue_from_push_ups"].sum()}")
print(f"Unknown categories listings: {unknown_data["number_of_listings"].sum()}")
print(f"Percentage of total revenue: {unknown_data["revenue_from_push_ups"].sum() / pricing_data_df["revenue_from_push_ups"].sum() * 100:.2f}%")
print(f"Percentage of total listings: {unknown_data["number_of_listings"].sum() / pricing_data_df["number_of_listings"].sum() * 100:.2f}% ")
print(f"Unknown categories usage of push-ups: {((unknown_data["revenue_from_push_ups"].sum())/2) / unknown_data["number_of_listings"].sum()* 100:.2f}%")
print("-" * 150)

#Filling NULL values in revenue from push ups and removing rows with NULL categories
pricing_data_df["revenue_from_push_ups"] = pricing_data_df["revenue_from_push_ups"].fillna(0)
pricing_data_df = pricing_data_df.dropna(subset=["category_3"])

#Checking how many unique category_2 values remained after cleaning the dataset
original_df = pd.read_csv("Vinted_technical_task/pricing_data.csv") 
print(f"Unique category_2 in original dataset: {original_df["category_2"].nunique()}\nUnique category_2 in dataset after cleaning: {pricing_data_df["category_2"].nunique()}")
print("-" * 150)

df_null = pricing_data_df.isna().sum()  # checking again for NULL values after handling it
print(df_null)
print("-" * 150)
print(f" Rows remaining in the dataset after cleaning it: {pricing_data_df.shape[0]}")
print("-" * 150)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Sub-categories diversification in main categories
grouped_by_category2 = pricing_data_df.groupby("category_2")["category_3"].count().reset_index()
grouped_by_category2.rename(columns={"category_3": "Count"}, inplace=True)
grouped_by_category2 = grouped_by_category2.sort_values("Count", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=grouped_by_category2, x="Count", y="category_2", palette="coolwarm", legend=False)
plt.title("Number of sub-categories per main category", fontsize=16)
plt.xlabel("Sub-categories", fontsize=12)
plt.ylabel("Main Categories", fontsize=12)
for container in plt.gca().containers:
    plt.gca().bar_label(container, fmt="%.0f")
plt.show()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Analysis of category distribution by revenue share and listings share
category_distribution = pricing_data_df.groupby("category_2").agg({
    "number_of_listings": "sum",
    "revenue_from_push_ups": "sum",
    "avg_listing_price_eur" : "mean"
}).sort_values("number_of_listings", ascending=False)

category_distribution["listings_share"] = (
    category_distribution["number_of_listings"] / 
    pricing_data_df["number_of_listings"].sum() * 100)

category_distribution["revenue_share"] = (
    category_distribution["revenue_from_push_ups"] /
    pricing_data_df["revenue_from_push_ups"].sum() * 100)


print(category_distribution)
print("-" * 150)

top5 = category_distribution.head(5)
others_listings_share = 100 - top5["listings_share"].sum()
others_revenue_share = 100 - top5["revenue_share"].sum()

listings_data = list(top5["listings_share"].values) + [others_listings_share]
revenue_data = list(top5["revenue_share"].values) + [others_revenue_share]
labels = list(top5.index) + ["Others"]

colors = ["#ff9999", "#66b3ff", "#99ffc7", "#ffcc99", "#ff99cc", "#d4d4d4"]

#1st chart representing the share of listings
fig1, ax1 = plt.subplots(figsize=(10, 8))

wedges1, texts1, autotexts1 = ax1.pie(
    listings_data, 
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    textprops={"fontsize": 11}
)

ax1.set_title("Top 5 Categories by Listings Share\n(% of Total Platform Listings)", 
              fontsize=14, fontweight="bold", pad=20)

for autotext in autotexts1:
    autotext.set_color("black")
    autotext.set_fontweight("bold")

plt.tight_layout()
plt.show()

#2nd chart representing the share of revenue
fig2, ax2 = plt.subplots(figsize=(10, 8))

wedges2, texts2, autotexts2 = ax2.pie(
    revenue_data, 
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    textprops={"fontsize": 11}
)

ax2.set_title("Top 5 Categories by Revenue Share\n(% of Total Push-up Revenue)", 
              fontsize=14, fontweight="bold", pad=20)

for autotext in autotexts2:
    autotext.set_color("black")
    autotext.set_fontweight("bold")

plt.tight_layout()
plt.show()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Visualzing the skewness of the dataset
ig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].hist(pricing_data_df["revenue_from_push_ups"], bins=30, color="skyblue", edgecolor="black")
axes[0].set_title("Revenue Distribution")
axes[0].set_xlabel("Revenue (€)")

axes[1].hist(pricing_data_df["number_of_listings"], bins=30, color="lightcoral", edgecolor="black")
axes[1].set_title("Listings Distribution")
axes[1].set_xlabel("Number of Listings")

axes[2].hist(pricing_data_df["avg_listing_price_eur"], bins=30, color="lightgreen", edgecolor="black")
axes[2].set_title("Price Distribution")
axes[2].set_xlabel("Average Price (€)")

plt.tight_layout()
plt.show()

revenue_skew = stats.skew(pricing_data_df["revenue_from_push_ups"])
listings_skew = stats.skew(pricing_data_df["number_of_listings"])
price_skew = stats.skew(pricing_data_df["avg_listing_price_eur"])

print(f"Revenue skewness: {revenue_skew:.2f} \nListings skewness: {listings_skew:.2f} \nPrice skewness: {price_skew:.2f}")
print("-" * 150)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Analysis of push-up feature usage 

total_listings = pricing_data_df["number_of_listings"].sum()
total_revenue_from_push_ups = pricing_data_df["revenue_from_push_ups"].sum()
times_of_push_ups_used = total_revenue_from_push_ups / push_up_price
ratio_of_push_up_per_item = times_of_push_ups_used / total_listings * 100
push_up_per_item = total_listings / times_of_push_ups_used 

print(f"The total listings: {total_listings}")
print(f"The total revenue from pricing push ups: {total_revenue_from_push_ups}")
print(f"Times that push up has been used by seller: {int(times_of_push_ups_used)}")
print("-" * 150)
print(f"Push up ratio per item: {round(ratio_of_push_up_per_item,2)} % \nPush up usage per item: 1 in {int(round(push_up_per_item,0))} items")
print("-" * 150)


fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

ax.text(5, 9, "Push-up Feature Usage Overview", 
        fontsize=22, fontweight="bold", ha="center")

rect1 = mpatches.FancyBboxPatch((0.3, 6), 2.8, 2, 
                                boxstyle="round,pad=0.15", 
                                edgecolor="#3498db", 
                                facecolor="#e3f2fd", 
                                linewidth=2)
ax.add_patch(rect1)
ax.text(1.7, 7.5, "Total Listings", 
        fontsize=12, fontweight="bold", ha="center")
ax.text(1.7, 6.8, f"{total_listings:,}", 
        fontsize=16, fontweight="bold", ha="center", color="#3498db")

rect2 = mpatches.FancyBboxPatch((3.6, 6), 2.8, 2, 
                                boxstyle="round,pad=0.15", 
                                edgecolor="#e74c3c", 
                                facecolor="#ffebee", 
                                linewidth=2)
ax.add_patch(rect2)
ax.text(5, 7.5, "Total Revenue", 
        fontsize=12, fontweight="bold", ha="center")
ax.text(5, 6.8, f"€{total_revenue_from_push_ups:,.0f}", 
        fontsize=16, fontweight="bold", ha="center", color="#e74c3c")

rect3 = mpatches.FancyBboxPatch((6.9, 6), 2.8, 2, 
                                boxstyle="round,pad=0.15", 
                                edgecolor="#27ae60", 
                                facecolor="#e8f8f5", 
                                linewidth=2)
ax.add_patch(rect3)
ax.text(8.3, 7.5, "Push-ups Used", 
        fontsize=12, fontweight="bold", ha="center")
ax.text(8.3, 6.8, f"{int(times_of_push_ups_used):,}", 
        fontsize=16, fontweight="bold", ha="center", color="#27ae60")

rect4 = mpatches.FancyBboxPatch((2.5, 3), 5, 2.3, 
                                boxstyle="round,pad=0.15", 
                                edgecolor="#9b59b6", 
                                facecolor="#f4ecf7", 
                                linewidth=3)
ax.add_patch(rect4)
ax.text(5, 4.7, "Push-up Adoption Rate", 
        fontsize=14, fontweight="bold", ha="center")
ax.text(5, 4, f"{ratio_of_push_up_per_item:.2f}%", 
        fontsize=24, fontweight="bold", ha="center", color="#9b59b6")
ax.text(5, 3.4, f"(1 in {int(round(push_up_per_item,0))} items)", 
        fontsize=12, ha="center", color="#6c3483", style="italic")

ax.text(5, 1.5, f"Note: Calculated based on €{push_up_price} per push-up usage", 
        fontsize=10, ha="center", style="italic", color="gray")

plt.tight_layout()
plt.show()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Based on the push-up adoption rate, calculating which categories performed well and which did not
# Calculate average price and adoption rate by category


grouped_by_category2_ratio = pricing_data_df.groupby("category_2").agg({
    "number_of_listings" : "sum",
    "revenue_from_push_ups" : "sum",
    "avg_listing_price_eur" : "mean"   
})

grouped_by_category2_ratio["push_ups_used"] = grouped_by_category2_ratio["revenue_from_push_ups"] / push_up_price

grouped_by_category2_ratio["adoption_rate_%"] = (
    grouped_by_category2_ratio["push_ups_used"] / 
    grouped_by_category2_ratio["number_of_listings"] * 100
).round(2)

grouped_by_category2_ratio["push_up_%_of_price"] = (
    push_up_price /  grouped_by_category2_ratio["avg_listing_price_eur"] * 100
).round(2)

grouped_by_category2_ratio = grouped_by_category2_ratio.sort_values("adoption_rate_%", ascending=False) 

print(grouped_by_category2_ratio)


top5 = grouped_by_category2_ratio.head(5)
bottom5 = grouped_by_category2_ratio.tail(5)

# Best 5 performers chart
fig1, ax1 = plt.subplots(figsize=(12, 7))

x_top = range(len(top5))
bars_top = ax1.barh(x_top, top5["adoption_rate_%"], color="#27ae60", alpha=0.7)
ax1.set_yticks(x_top)
ax1.set_yticklabels(top5.index, fontsize=11, fontweight="bold")
ax1.set_xlabel("Adoption Rate (%)", fontsize=12, fontweight="bold")
ax1.set_title("Top 5 Categories by Push-up Adoption Rate", fontsize=14, fontweight="bold", pad=20)
ax1.invert_yaxis()

for i, (bar, rate, price, listings) in enumerate(zip(bars_top, top5["adoption_rate_%"], 
                                                       top5["avg_listing_price_eur"],
                                                       top5["number_of_listings"])):
    ax1.text(bar.get_width() * 0.5, bar.get_y() + bar.get_height()/2, 
            f"adoption rate: {rate:.2f}%\n€{price:.2f} average price\n{listings:,} items",
            va="center", ha="center", fontsize=10, fontweight="bold", color="white")

ax1.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# Worst 5 performers
fig2, ax2 = plt.subplots(figsize=(12, 7))

x_bottom = range(len(bottom5))
bars_bottom = ax2.barh(x_bottom, bottom5["adoption_rate_%"], color="#e74c3c", alpha=0.7)
ax2.set_yticks(x_bottom)
ax2.set_yticklabels(bottom5.index, fontsize=11, fontweight="bold")
ax2.set_xlabel("Adoption Rate (%)", fontsize=12, fontweight="bold")
ax2.set_title("Bottom 5 Categories by Push-up Adoption Rate", fontsize=14, fontweight="bold", pad=20)
ax2.invert_yaxis()

max_rate = bottom5["adoption_rate_%"].max()
ax2.set_xlim(0, max_rate * 2.2) 

for i, (bar, rate, price, listings) in enumerate(zip(bars_bottom, bottom5["adoption_rate_%"], 
                                                       bottom5["avg_listing_price_eur"],
                                                       bottom5["number_of_listings"])):
    if bar.get_width() < max_rate * 0.3:
        ax2.text(bar.get_width() + max_rate * 0.05, bar.get_y() + bar.get_height()/2, 
                f"adoption rate: {rate:.2f}%\n€{price:.2f} average price\n{listings:,} items",
                va="center", ha="left", fontsize=10, fontweight="bold")
    else:
        ax2.text(bar.get_width() * 0.5, bar.get_y() + bar.get_height()/2, 
                f"adoption rate: {rate:.2f}%\n€{price:.2f} average price\n{listings:,} items",
                va="center", ha="center", fontsize=10, fontweight="bold", color="white")

ax2.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Another metric to analyse the push-up usage (Which categories have the biggest burden of the push-up)
# Checking the correlation between two metrics
corr_value = grouped_by_category2_ratio["adoption_rate_%"].corr(grouped_by_category2_ratio["push_up_%_of_price"])

plt.figure(figsize=(8,6))
sns.regplot(
    data=grouped_by_category2_ratio,
    x="push_up_%_of_price",
    y="adoption_rate_%",
    scatter_kws={"alpha":0.6},
    line_kws={"color":"red"}
)

plt.title("Correlation between Push-up Cost (% of Item Price) and Adoption Rate")
plt.xlabel("Push-Up % of Price")
plt.ylabel("Adoption Rate (%)")

plt.text(
    x=grouped_by_category2_ratio["push_up_%_of_price"].max(),  
    y=grouped_by_category2_ratio["adoption_rate_%"].max(),    
    s=f"Correlation: {corr_value:.2f}",
    fontsize=12,
    color="blue",
    ha="right",
    va="top"
)

plt.show()

grouped_by_category2_ratio = grouped_by_category2_ratio.sort_values("push_up_%_of_price", ascending=False) 

top5_1 = grouped_by_category2_ratio.head(5)
bottom5_1 = grouped_by_category2_ratio.tail(5)

# Top 5 categories with highest push-up percentages of average price
fig1, ax1 = plt.subplots(figsize=(12, 7))

x_top = range(len(top5_1))
bars_top = ax1.barh(x_top, top5_1["push_up_%_of_price"], color="#27ae60", alpha=0.7)
ax1.set_yticks(x_top)
ax1.set_yticklabels(top5_1.index, fontsize=11, fontweight="bold")
ax1.set_xlabel("Push-Up Percentage of Price (%)", fontsize=12, fontweight="bold")
ax1.set_title("Top 5 Categories with highest Push-Up % of Average Price", fontsize=14, fontweight="bold", pad=20)
ax1.invert_yaxis()

for i, (bar, rate, percentage, price) in enumerate(zip(bars_top, top5_1["adoption_rate_%"], 
                                                       top5_1["push_up_%_of_price"],
                                                       top5_1["avg_listing_price_eur"])): 
    ax1.text(bar.get_width() * 0.5, bar.get_y() + bar.get_height()/2, 
            f"adoption rate: {rate:.2f}%\n% of avg_price: {percentage:.2f}%\n€{price:.2f} average price",
            va="center", ha="center", fontsize=10, fontweight="bold", color="white")

ax1.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# Bottom 5 categories with lowest push-up percentages of average price
fig2, ax2 = plt.subplots(figsize=(12, 7))

x_bottom = range(len(bottom5_1))
bars_bottom = ax2.barh(x_bottom, bottom5_1["push_up_%_of_price"], color="#e74c3c", alpha=0.7)
ax2.set_yticks(x_bottom)
ax2.set_yticklabels(bottom5_1.index, fontsize=11, fontweight="bold")
ax2.set_xlabel("Push-Up Percentage of Price (%)", fontsize=12, fontweight="bold")
ax2.set_title("Bottom 5 Categories with lowest Push-Up % of Average Price", fontsize=14, fontweight="bold", pad=20)
ax2.invert_yaxis()

max_rate = bottom5_1["push_up_%_of_price"].max()
ax2.set_xlim(0, max_rate * 2.2) 

for i, (bar, rate, percentage, price) in enumerate(zip(bars_bottom, bottom5_1["adoption_rate_%"], 
                                                       bottom5_1["push_up_%_of_price"],
                                                       bottom5_1["avg_listing_price_eur"])): 
    if bar.get_width() < max_rate * 0.3:
        ax1.text(bar.get_width() * 0.5, bar.get_y() + bar.get_height()/2, 
            f"adopt rate: {rate:.2f}%\n% avg_price: {percentage:.2f}%\n€{price:.2f} avg price",
            va="center", ha="center", fontsize=10, fontweight="bold", color="white")
    else:
        ax2.text(bar.get_width() * 0.5, bar.get_y() + bar.get_height()/2, 
            f"adopt rate: {rate:.2f}%\n% avg_price: {percentage:.2f}%\n€{price:.2f} avg price",
            va="center", ha="center", fontsize=10, fontweight="bold", color="white")
        
ax2.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------