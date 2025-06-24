import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Load data
df = pd.read_csv("BI&A - Case Study Dataset.csv")

# Clean data
df = df.dropna(subset=["duration_watched(minutes)", "show_watched", "device_used", "rating_given", "gender", "subscription_type", "watching_method", "age"])
df["Month Name"] = pd.Categorical(df["Month Name"], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"], ordered=True)
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 25, 35, 50, 100], labels=["<18", "18-25", "26-35", "36-50", "50+"])

# Sidebar with logo
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=100)
st.sidebar.header("📊 Customize Your View")
selected_location = st.sidebar.multiselect("Select Location", options=df["location"].unique(), default=df["location"].unique())
selected_watch = st.sidebar.multiselect("Select Watching Method", options=df["watching_method"].unique(), default=df["watching_method"].unique())
selected_subscription = st.sidebar.multiselect("Select Subscription Type", options=df["subscription_type"].unique(), default=df["subscription_type"].unique())

# Apply filters
filtered_df = df[
    (df["location"].isin(selected_location)) &
    (df["watching_method"].isin(selected_watch)) &
    (df["subscription_type"].isin(selected_subscription))
]

# Title (medium size)
st.markdown("<h2 style='color: #E50914; font-family:Helvetica;'>Netflix User Analytics Dashboard</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #E50914;'>", unsafe_allow_html=True)

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    binge_pct = (filtered_df[filtered_df["watching_method"] == "Binge-watched"].shape[0] / filtered_df.shape[0]) * 100
    st.metric("🎯 % Binge Viewers", f"{binge_pct:.1f}%")
with col2:
    avg_duration = filtered_df["duration_watched(minutes)"].mean()
    st.metric("⏱ Avg Watch Duration", f"{avg_duration:.1f} mins")
with col3:
    avg_rating = filtered_df["rating_given"].mean()
    st.metric("⭐ Avg Rating", f"{avg_rating:.1f}/5")

# Top Shows - Bar Chart (Descending)
st.subheader("🏆 Top Watched Shows (Sorted by Views)")
top_shows = filtered_df.groupby("show_watched").agg({
    "user_id": "count",
    "duration_watched(minutes)": "mean"
}).rename(columns={"user_id": "Count of Views", "duration_watched(minutes)": "Avg Duration"}).reset_index()
top_shows = top_shows.sort_values(by="Count of Views", ascending=False).head(10)
fig_top = px.bar(top_shows, y="show_watched", x="Count of Views", color="Avg Duration",
                 orientation="h", color_continuous_scale="Reds", hover_data=["Avg Duration"])
fig_top.update_layout(xaxis_title="Views", yaxis_title="Show", yaxis=dict(autorange="reversed"))
st.plotly_chart(fig_top)

# Subscription Type View
st.subheader("💼 Subscription Type vs Watching Method")
sub_watch = filtered_df.groupby(["subscription_type", "watching_method"]).agg({
    "duration_watched(minutes)": "mean",
    "user_id": pd.Series.nunique
}).reset_index().rename(columns={
    "duration_watched(minutes)": "Avg Duration",
    "user_id": "Unique Viewers"
})
fig_subwatch = px.bar(sub_watch, x="subscription_type", y="Avg Duration", color="watching_method",
                      barmode="group", text="Unique Viewers",
                      title="Average Duration by Subscription Type & Watching Method",
                      hover_data=["Unique Viewers"])
fig_subwatch.update_layout(xaxis_title="Subscription Type", yaxis_title="Avg Duration (mins)")
st.plotly_chart(fig_subwatch)

# Device Pie Chart (unchanged)
st.subheader("📱 Device Usage with Avg Duration (Colored by Unique Viewers)")
device_data = filtered_df.groupby("device_used").agg({
    "duration_watched(minutes)": "mean",
    "user_id": pd.Series.nunique
}).reset_index().rename(columns={"duration_watched(minutes)": "Avg Duration", "user_id": "Unique Viewers"})
fig_device = px.pie(device_data, names="device_used", values="Avg Duration", 
                    color="Unique Viewers", title="Device Usage - Avg Duration Colored by Unique Viewers",
                    hole=0.4)
st.plotly_chart(fig_device)

# Monthly Viewership Trend
st.subheader("📈 Monthly Viewership Trend")
monthly_trend = filtered_df.groupby("Month Name")["user_id"].count().reset_index(name="View Count")
fig_line = px.line(monthly_trend, x="Month Name", y="View Count", markers=True, title="Monthly Viewership (Jan–Jul)")
st.plotly_chart(fig_line)

# Age Group Duration View (Line by Age Group & Gender)
st.subheader("👥 Gender vs Age Group - Duration Watched (Line), Tooltip with Viewer Count")
age_gender_data = filtered_df.groupby(["gender", "age_group"]).agg({
    "duration_watched(minutes)": "mean",
    "user_id": pd.Series.nunique
}).reset_index().rename(columns={"duration_watched(minutes)": "Avg Duration", "user_id": "Unique Viewers"})

fig_age = px.line(age_gender_data, x="age_group", y="Avg Duration", color="gender", markers=True,
                  line_shape="linear", hover_data=["Unique Viewers"],
                  title="")
fig_age.update_layout(xaxis_title="Age Group", yaxis_title="Avg Duration")
st.plotly_chart(fig_age)

# Map View
st.subheader("🌍 Map - Average Duration by Location")
map_data = filtered_df.groupby("location").agg({
    "duration_watched(minutes)": "mean",
    "user_id": pd.Series.nunique
}).reset_index().rename(columns={"duration_watched(minutes)": "Avg Duration", "user_id": "Unique Viewers"})
map_data["Avg Duration"] = map_data["Avg Duration"].round(1)
fig_map = px.choropleth(map_data, locations="location", locationmode="country names",
                        color="Avg Duration", hover_data=["Unique Viewers"],
                        color_continuous_scale="Oranges", title="Avg Duration Watched by Country")
st.plotly_chart(fig_map)
