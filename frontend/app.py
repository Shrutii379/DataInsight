
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api import get_filter_options, get_dashboard_data


# 1. Page Configuration
st.set_page_config(
    page_title="DataInsight",
    page_icon="📊",
    layout="wide"
)


# 2. Dashboard Title
st.title("📊 DataInsight")
st.subheader("E-Commerce Analytics Dashboard")


try:

    # 3. Fetch Filter Options
    filters = get_filter_options()

    # 4. Sidebar Filters
    st.sidebar.title("Dashboard Filters")

    selected_year = st.sidebar.selectbox(
        "Select Year",
        ["All"] + filters["years"]
    )

    selected_country = st.sidebar.selectbox(
        "Select Country",
        ["All"] + filters["countries"]
    )

    # 5. Convert All into None
    year = None if selected_year == "All" else int(selected_year)

    country = (
        None if selected_country == "All"
        else selected_country
    )

    # 6. Fetch Filtered Dashboard Data
    dashboard = get_dashboard_data(
        year=year,
        country=country
    )

    st.success("Dashboard data loaded successfully!")

    # 7. Professional KPI Cards
    data = dashboard["kpis"]

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(
            f"""
            <div style="background-color:#E8F0FE;padding:20px;border-radius:12px;">
                <h4 style="color:#1A73E8;">💰 Total Revenue</h4>
                <h2 style="color:#174EA6;">₹{data['total_revenue']:,.2f}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background-color:#E6F4EA;padding:20px;border-radius:12px;">
                <h4 style="color:#188038;">📦 Total Orders</h4>
                <h2 style="color:#137333;">{data['total_orders']:,}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="background-color:#FCE8E6;padding:20px;border-radius:12px;">
                <h4 style="color:#D93025;">👥 Total Customers</h4>
                <h2 style="color:#B3261E;">{data['total_customers']:,}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div style="background-color:#FEF7E0;padding:20px;border-radius:12px;">
                <h4 style="color:#B06000;">🛍️ Total Products</h4>
                <h2 style="color:#8D4B00;">{data['total_products']:,}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        st.markdown(
            f"""
            <div style="background-color:#F3E8FF;padding:20px;border-radius:12px;">
                <h4 style="color:#7E22CE;">📊 Average Order Value</h4>
                <h2 style="color:#6B21A8;">₹{dashboard['average_order_value']:,.2f}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Repeat Customers Card
    with col6:
        st.markdown(
            f"""
            <div style="background-color:#E0F2F1;padding:20px;border-radius:12px;">
                <h4 style="color:#00796B;">🔁 Repeat Customers</h4>
                <h2 style="color:#004D40;">{dashboard['repeat_customers']:,}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Repeat Purchase Rate Card - Second Row
    st.write("")

    with st.container():
        st.markdown(
            f"""
            <div style="background-color:#FFF3E0;padding:20px;border-radius:12px;">
                <h4 style="color:#E65100;">🔄 Repeat Purchase Rate</h4>
                <h2 style="color:#BF360C;">{dashboard['repeat_purchase_rate']:.2f}%</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # 8. Monthly Revenue Chart
    st.subheader("📈 Monthly Revenue Trend")

    monthly_df = pd.DataFrame(
        dashboard["monthly_revenue"]
    )

    if not monthly_df.empty:

        monthly_df["Period"] = (
            monthly_df["Year"].astype(str)
            + "-"
            + monthly_df["Month"].astype(str).str.zfill(2)
        )

        fig = px.line(
            monthly_df,
            x="Period",
            y="revenue",
            markers=True,
            title="Monthly Revenue Analysis",
            labels={
                "Period": "Month",
                "revenue": "Revenue"
            },
            template="plotly_white"
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate="Month: %{x}<br>Revenue: %{y:,.2f}<extra></extra>"
        )

        fig.update_layout(
            height=450,
            xaxis_title="Month",
            yaxis_title="Revenue",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No monthly revenue data available.")

    st.divider()

    # 9. Top 10 Products Chart
    st.subheader("🏆 Top 10 Products by Revenue")

    products_df = pd.DataFrame(
        dashboard["top_products"]
    )

    if not products_df.empty:

        fig = px.bar(
            products_df,
            x="total_revenue",
            y="Description",
            orientation="h",
            title="Top 10 Products by Revenue",
            labels={
                "total_revenue": "Revenue",
                "Description": "Product"
            },
            template="plotly_white"
        )

        fig.update_layout(
            height=500,
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No product data available.")

    st.divider()

    # 10. Top Countries Chart
    st.subheader("🌍 Top Countries by Revenue")

    countries_df = pd.DataFrame(
        dashboard["top_countries"]
    )

    if not countries_df.empty:

        fig = px.bar(
            countries_df,
            x="Country",
            y="total_revenue",
            title="Top Countries by Revenue",
            labels={
                "Country": "Country",
                "total_revenue": "Revenue"
            },
            template="plotly_white"
        )

        fig.update_layout(
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No country data available.")

    st.divider()


            # 11. Business Insights
    st.subheader("💡 Business Insights")

    insight1, insight2, insight3, insight4 = st.columns(4)

    # Insight 1: Highest Revenue Country
    with insight1:
        if dashboard["top_countries"]:
            top_country = dashboard["top_countries"][0]

            st.metric(
                label="🌍 Highest Revenue Country",
                value=top_country["Country"],
                delta=f"₹{top_country['total_revenue']:,.2f} Revenue"
            )

    # Insight 2: Top Performing Product
    with insight2:
        if dashboard["top_products"]:
            top_product = dashboard["top_products"][0]

            st.metric(
                label="🏆 Top Performing Product",
                value=top_product["StockCode"],
                help=top_product["Description"]
            )

    # Insight 3: Repeat Customers
    with insight3:
        st.metric(
            label="🔁 Repeat Customers",
            value=f"{dashboard['repeat_customers']:,}"
        )

    # Insight 4: Repeat Purchase Rate
    with insight4:
        st.metric(
            label="📊 Repeat Purchase Rate",
            value=f"{dashboard['repeat_purchase_rate']:.2f}%"
        )

    st.divider()

    
    # 11. Professional Customer Analysis
    st.subheader("👥 Top 10 Customers")

    customer_df = pd.DataFrame(
        dashboard["customer_analysis"]
    )

    if not customer_df.empty:

        customer_df.insert(
            0,
            "Rank",
            range(1, len(customer_df) + 1)
        )

        customer_df = customer_df.rename(
            columns={
                "total_orders": "Total Orders",
                "total_revenue": "Total Revenue",
                "total_quantity": "Total Quantity"
            }
        )

        customer_df["Total Revenue"] = customer_df[
            "Total Revenue"
        ].apply(lambda x: f"₹{x:,.2f}")

        st.dataframe(
            customer_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No customer data available.")


except Exception as e:
    st.error(f"Error loading dashboard: {e}")
