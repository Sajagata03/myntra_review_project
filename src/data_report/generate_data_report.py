import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os, sys
from src.exception import CustomException


class DashboardGenerator:
    def __init__(self, data):
        self.data = data
    # the 'data' is coming from scraped data
    def display_general_info(self):
        st.header('General Information')

        # Convert 'Over_All_Rating' and 'Price' columns to numeric
        self.data['Over_All_Rating'] = pd.to_numeric(self.data['Over_All_Rating'], errors='coerce')
        self.data['Price'] = pd.to_numeric(
            self.data['Price'].apply(lambda x: x.replace("₹", "")),
            errors='coerce')

        self.data["Rating"] = pd.to_numeric(self.data['Rating'], errors='coerce')

        # Summary pie chart of average ratings by product
        '''product_ratings = self.data.groupby('Product Name', as_index=False)['Over_All_Rating'].mean().dropna()

        fig_pie = px.pie(product_ratings, values='Over_All_Rating', names='Product Name',
                         title='Average Ratings by Product')
        st.plotly_chart(fig_pie)'''
        product_ratings = self.data.groupby('Product Name', as_index=False)['Over_All_Rating'].mean().dropna()
        
        if len(product_ratings) > 1:
            fig_bar = px.bar(
                product_ratings,
                x='Product Name',
                y='Over_All_Rating',
                color='Product Name',
                title='Average Ratings by Product'
            )
            fig_bar.update_xaxes(showticklabels=False)

            st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("### Products:")
            for i, name in enumerate(product_ratings['Product Name'], start=1):
                st.write(f"➡️ **P{i}** – {name}")


        # ================= EXTRA VISUALIZATIONS =================

        # KPI row
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Overall Avg Price (₹)", round(self.data['Price'].mean(), 2))

        with col2:
            st.metric("Overall Avg Rating ⭐", round(self.data['Over_All_Rating'].mean(), 2))

        with col3:
            st.metric("Total Products", self.data['Product Name'].nunique())


        # Two-column layout
        col4, col5 = st.columns(2)

        with col4:
            fig_hist = px.histogram(
                self.data,
                x='Price',
                nbins=20,
                title='Price Distribution'
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with col5:
            fig_scatter = px.scatter(
                self.data,
                x='Price',
                y='Over_All_Rating',
                color='Product Name',
                title='Price vs Rating',
                hover_data=['Product Name']
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Box plot for rating spread
        fig_box = px.box(
            self.data,
            x='Product Name',
            y='Over_All_Rating',
            title='Rating Distribution by Product'
        )
        fig_box.update_xaxes(showticklabels=False)

        st.plotly_chart(fig_box, use_container_width=True)


        # Bar chart comparing average prices of different products with different colors
        # Bar chart comparing average prices of different products
        avg_prices = self.data.groupby('Product Name', as_index=False)['Price'].mean().dropna()
        fig_bar = px.bar(
            avg_prices,
            x='Product Name',
            y='Price',
            color='Product Name',
            title='Average Price Comparison Between Products',
            color_discrete_sequence=px.colors.qualitative.Bold
        )

        # Hide ugly long labels
        fig_bar.update_xaxes(showticklabels=False)
        fig_bar.update_yaxes(title='Average Price')

        st.plotly_chart(fig_bar, use_container_width=True)

        # Show clean mapping below the chart
        st.markdown("### Products:")
        for i, name in enumerate(avg_prices['Product Name'], start=1):
            st.write(f"➡️ **P{i}** – {name}")


    def display_product_sections(self):
        st.header('Product Sections')

        product_names = self.data['Product Name'].unique()
        columns = st.columns(len(product_names))

        for i, product_name in enumerate(product_names):
            product_data = self.data[self.data['Product Name'] == product_name]

            with columns[i]:
                st.subheader(f'{product_name}')

                # Display price in text or markdown with emojis
                avg_price = product_data['Price'].mean()
                st.markdown(f"💰 Average Price: ₹{avg_price:.2f}")

                # Display average rating
                avg_rating = product_data['Over_All_Rating'].mean()
                st.markdown(f"⭐ Average Rating: {avg_rating:.2f}")

                # Display top positive comments with great ratings
                positive_reviews = product_data[product_data['Rating'] >= 4.5].nlargest(5, 'Rating')
                st.subheader('Positive Reviews')
                for index, row in positive_reviews.iterrows():
                    st.markdown(f"✨ Rating: {row['Rating']} - {row['Comment']}")

                # Display top negative comments with worst ratings
                negative_reviews = product_data[product_data['Rating'] <= 2].nsmallest(5, 'Rating')
                st.subheader('Negative Reviews')
                for index, row in negative_reviews.iterrows():
                    st.markdown(f"💢 Rating: {row['Rating']} - {row['Comment']}")

                # Display rating counts in different categories
                st.subheader('Rating Counts')
                rating_counts = product_data['Rating'].value_counts().sort_index(ascending=False)
                for rating, count in rating_counts.items():
                    st.write(f"🔹 Rating {rating} count: {count}")
