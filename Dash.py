import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- 1. PAGE CONFIGURATION & CUSTOM THEME ---
st.set_page_config(
    page_title="Smart Energy Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern, professional color palette
PRIMARY_COLOR = "#264653"
SECONDARY_COLOR = "#2A9D8F"
ACCENT_COLOR = "#E9C46A"
BACKGROUND_COLOR = "#F0F2F6"
TEXT_COLOR = "#333333"

# Inject custom CSS for a polished look
def set_custom_style():
    st.markdown(f"""
    <style>
        /* Main App Background */
        .main {{
            background-color: {BACKGROUND_COLOR};
        }}
        
        /* Top-level Headers (h1, h2, h3) */
        h1, h2, h3 {{
            color: {PRIMARY_COLOR} !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 600;
        }}
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: {PRIMARY_COLOR};
        }}
        
        /* Sidebar text and headers */
        section[data-testid="stSidebar"] .css-1lcbmhc {{
            color: white;
        }}
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {{
            color: #E9C46A !important; /* Accent color for sidebar headers */
        }}
        
        /* All text in sidebar */
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label {{
            color: #F0F2F6 !important;
        }}
        
        /* Main titles in the app body */
        .stTitle {{
            border-bottom: 2px solid {SECONDARY_COLOR};
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        /* Metric containers */
        .stMetric {{
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-left: 4px solid {SECONDARY_COLOR};
        }}
        
        /* Button styling */
        .stButton>button {{
            background-color: {SECONDARY_COLOR};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 24px;
            font-weight: 600;
        }}
        .stButton>button:hover {{
            background-color: #21867A;
        }}
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: white;
            border-radius: 4px 4px 0 0;
            padding: 10px 20px;
            color: {PRIMARY_COLOR};
            font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {PRIMARY_COLOR};
            color: white;
        }}
        
        /* Dataframes */
        .stDataFrame {{
            border: none !important;
        }}
        
        /* Card-like containers for recommendations */
        .recommendation-card {{
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border-left: 4px solid {ACCENT_COLOR};
        }}
    </style>
    """, unsafe_allow_html=True)

set_custom_style()


# --- 2. DASHBOARD HEADER & DESCRIPTION ---
st.title("⚡ Smart Energy Dashboard")
st.markdown("""
**Monitor, analyze, and optimize your building's energy consumption in real-time.**  
This dashboard serves as a central hub for managing energy usage, identifying inefficiencies, and acting on AI-driven recommendations to reduce costs and environmental impact.
""")
st.markdown("---") # Horizontal rule


# --- 3. LOAD AND PREPARE DATA ---

# A. Equipment Data (from user input)
equipment_data = {
    'Category': ['Personal Devices', 'Personal Devices', 'Personal Devices', 'Personal Devices', 'Personal Devices', 'Personal Devices',
                 'Kitchen', 'Kitchen', 'Kitchen', 'Kitchen'],
    'Equipment': ['Laptop Charger', 'Phone Charger', 'Mini Fridge', 'Electric Kettle', 'Microwave', 'Air Fryer', 'Toaster',
                  'Fridge', 'Oven', 'Hot Plate'],
    'Power Rated (kW)': [0.065, 0.01, 0.08, 1.8, 1.2, 1.4, 0.8, 0.15, 2, 1.2],
    'Simultaneity Factor': [0.6, 0.5, 0.8, 0.2, 0.1, 0.1, 0.2, 0.8, 0.3, 0.3],
    'Load Factor': [0.75, 0.75, 1, 0.75, 0.75, 0.75, 0.75, 1, 0.75, 0.75],
    'Quantity': [60, 60, 50, 55, 10, 35, 25, 2, 2, 4],
    'Adjusted Power (kW)': [1.755, 0.225, 3.2, 14.85, 0.9, 3.675, 3, 0.24, 0.9, 1.08],
    'Operating Time (h/day)': [6, 4, 24, 1.5, 1, 2, 1, 24, 3, 8],
    'Daily Energy Consumption (KWh)': [10.53, 0.9, 76.8, 22.275, 0.9, 7.35, 3, 5.76, 2.7, 8.64]
}
df_equipment = pd.DataFrame(equipment_data)
# Add a timestamp for "real-time" simulation
df_equipment['Last Updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# --- 4. SIDEBAR: USER CONFIGURATION ---
with st.sidebar:
    st.header("Building Configuration")
    st.markdown("Configure your building's details to enable personalized monitoring and AI insights.")
    
    building_name = st.text_input("Building Name", "Innovation Center")
    total_area = st.number_input("Total Area (sqm)", min_value=100, value=2500)
    num_rooms = st.number_input("Number of Rooms", min_value=1, value=50)
    
    st.markdown("### Energy Sources")
    energy_sources = st.multiselect(
        "Active Renewable Sources",
        ["Solar Panels", "Wind Turbines", "Geothermal", "Biomass"],
        default=["Solar Panels"]
    )
    
    st.markdown("---")
    st.info("Configure devices and sensors on the 'Configuration' tab.")


# --- 5. KEY METRICS (TOP ROW) ---
# Calculate key metrics
total_daily_consumption = df_equipment['Daily Energy Consumption (KWh)'].sum()
total_installed_capacity = df_equipment['Power Rated (kW)'].sum()
# Simulate a renewable energy contribution for the demo
renewable_contribution = 25.4 if "Solar Panels" in energy_sources else 0

# Create a row with 4 key metrics
kcol1, kcol2, kcol3, kcol4 = st.columns(4)
with kcol1:
    st.metric(label="Total Daily Consumption", value=f"{total_daily_consumption:,.2f} KWh", delta="1.2%")
with kcol2:
    st.metric(label="Renewable Energy Generated", value=f"{renewable_contribution:,.1f} KWh", delta="5.4%")
with kcol3:
    st.metric(label="Active Devices", value=f"{len(df_equipment)}", delta=None)
with kcol4:
    st.metric(label="Estimated Daily Cost", value=f"${total_daily_consumption * 0.12:,.2f}", delta="-2.1%")


# --- 6. MAIN DASHBOARD TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Analytics", "🤖 AI Recommendations", "⚙️ Configuration"])


# --- TAB 1: OVERVIEW ---
with tab1:
    st.subheader("Real-time Energy Monitoring")
    st.markdown("Live data from all sensors and devices across the building.")
    
    # Create two columns
    o_col1, o_col2 = st.columns([1.5, 1])
    
    with o_col1:
        st.markdown("#### Equipment Energy Consumption Details")
        # Display the dataframe with clean styling
        st.dataframe(
            df_equipment[['Category', 'Equipment', 'Quantity', 'Operating Time (h/day)', 'Daily Energy Consumption (KWh)', 'Last Updated']],
            use_container_width=True,
            height=450
        )
    
    with o_col2:
        st.markdown("#### Consumption Distribution")
        # Pie chart for energy by category
        category_consumption = df_equipment.groupby('Category')['Daily Energy Consumption (KWh)'].sum().reset_index()
        fig_pie = px.pie(
            category_consumption,
            values='Daily Energy Consumption (KWh)',
            names='Category',
            title='Energy Consumption by Category',
            hole=0.4,  # Donut chart for a modern look
            color_discrete_map={'Personal Devices': SECONDARY_COLOR, 'Kitchen': ACCENT_COLOR}
        )
        fig_pie.update_traces(textfont_size=14, textfont_color='white')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Highlight top consumers
        top_3 = df_equipment.nlargest(3, 'Daily Energy Consumption (KWh)')
        st.markdown("#### Top Consumers")
        for _, row in top_3.iterrows():
            st.markdown(f"""
            <div style="padding: 5px 0; border-bottom: 1px solid #eee;">
                <strong>{row['Equipment']}</strong><br/>
                <span style="color: {TEXT_COLOR};">Consumption: {row['Daily Energy Consumption (KWh)']:.2f} KWh</span>
            </div>
            """, unsafe_allow_html=True)


# --- TAB 2: ANALYTICS ---
with tab2:
    st.subheader("Energy Consumption Analytics")
    st.markdown("Visualize usage patterns, peak hours, and equipment performance.")
    
    # Chart 1: Bar chart of all equipment
    st.markdown("### Daily Energy Consumption by Equipment")
    fig_bar = px.bar(
        df_equipment.sort_values('Daily Energy Consumption (KWh)', ascending=False),
        x='Equipment',
        y='Daily Energy Consumption (KWh)',
        color='Category',
        title='Total Daily Energy Consumption (KWh)',
        text='Daily Energy Consumption (KWh)',
        color_discrete_map={'Personal Devices': SECONDARY_COLOR, 'Kitchen': ACCENT_COLOR}
    )
    # Enhance the bar chart appearance
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_bar.update_layout(
        xaxis_title="Equipment",
        yaxis_title="Energy (KWh)",
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        plot_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Chart 2: Scatter plot for relationships
    st.markdown("### Operating Time vs. Energy Consumption")
    fig_scatter = px.scatter(
        df_equipment,
        x='Operating Time (h/day)',
        y='Daily Energy Consumption (KWh)',
        color='Category',
        size='Quantity',
        hover_data=['Equipment', 'Power Rated (kW)'],
        title='Operating Time vs Energy Consumption',
        color_discrete_map={'Personal Devices': SECONDARY_COLOR, 'Kitchen': ACCENT_COLOR}
    )
    fig_scatter.update_layout(plot_bgcolor='white')
    st.plotly_chart(fig_scatter, use_container_width=True)


# --- TAB 3: AI RECOMMENDATIONS ---
with tab3:
    st.subheader("AI-Driven Energy Saving Recommendations")
    st.markdown("""
    Our AI module analyzes your data to identify inefficiencies and suggest actionable improvements. 
    Each recommendation includes potential energy savings, cost reduction, and environmental impact.
    """)
    
    # Generate mock AI recommendations based on the data
    recommendations = []
    
    # Identify top consumers for recommendations
    high_consumers = df_equipment.nlargest(3, 'Daily Energy Consumption (KWh)')
    
    for _, row in high_consumers.iterrows():
        rec = {
            'Device': row['Equipment'],
            'Current_Consumption': row['Daily Energy Consumption (KWh)'],
            'Suggestion': f"Optimize operation of {row['Equipment']}. Consider scheduling or upgrading to an energy-efficient model.",
            'Savings_Estimate': f"{row['Daily Energy Consumption (KWh)'] * 0.15:.2f} KWh/day",
            'Cost_Savings': f"${row['Daily Energy Consumption (KWh)'] * 0.15 * 0.12:.2f}/day",
            'CO2_Reduction': f"{row['Daily Energy Consumption (KWh)'] * 0.15 * 0.5:.2f} kg CO₂eq/day"
        }
        recommendations.append(rec)
    
    # Add a general recommendation about renewables
    if "Solar Panels" not in energy_sources:
        recommendations.append({
            'Device': "Building Energy System",
            'Current_Consumption': total_daily_consumption,
            'Suggestion': "Install solar panels to offset grid consumption during peak daylight hours.",
            'Savings_Estimate': f"{total_daily_consumption * 0.3:.2f} KWh/day",
            'Cost_Savings': f"${total_daily_consumption * 0.3 * 0.12:.2f}/day",
            'CO2_Reduction': f"{total_daily_consumption * 0.3 * 0.5:.2f} kg CO₂eq/day"
        })
    
    # Display recommendations in clean, card-like containers
    for i, rec in enumerate(recommendations):
        st.markdown(f"### Recommendation #{i+1}")
        with st.container():
            # Using columns to layout the recommendation nicely
            rc1, rc2 = st.columns([2, 1])
            
            with rc1:
                st.markdown(f"<div class='recommendation-card'>", unsafe_allow_html=True)
                st.markdown(f"**Device/System:** {rec['Device']}")
                st.markdown(f"**Suggestion:** {rec['Suggestion']}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with rc2:
                st.metric("Potential Energy Savings", rec['Savings_Estimate'])
                st.metric("Estimated Cost Savings", rec['Cost_Savings'])
                st.metric("Environmental Impact", rec['CO2_Reduction'])
        
        st.markdown("---")


# --- TAB 4: CONFIGURATION ---
with tab4:
    st.subheader("System Configuration")
    st.markdown("Define your building layout, devices, and sensor mappings.")
    
    st.markdown("### Add New Equipment")
    
    # Form for adding new equipment
    with st.form("equipment_form"):
        col1, col2 = st.columns(2)
        with col1:
            eq_name = st.text_input("Equipment Name")
            eq_category = st.selectbox("Category", ["Personal Devices", "Kitchen", "HVAC", "Lighting", "Special Equipment"])
            eq_quantity = st.number_input("Quantity", min_value=1)
        
        with col2:
            eq_power = st.number_input("Power Rating (kW)", min_value=0.0, format="%.3f")
            eq_op_time = st.number_input("Operating Time (h/day)", min_value=0.0, max_value=24.0, format="%.1f")
            eq_sim_factor = st.slider("Simultaneity Factor", 0.0, 1.0, 0.5)
        
        submitted = st.form_submit_button("Add Equipment")
        if submitted:
            st.success(f"Equipment '{eq_name}' has been added to the system!")
    
    st.markdown("---")
    st.markdown("### Building Layout Management")
    st.markdown("Upload building layout files or configure rooms manually.")
    uploaded_file = st.file_uploader("Upload Building Layout (Image or CAD File)", type=['png', 'jpg', 'jpeg', 'dxf'])
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Building Layout', use_column_width=True)


# --- 7. FOOTER ---
st.markdown("---")
footer_col1, footer_col2 = st.columns([2, 1])
with footer_col1:
    st.markdown(f"**Smart Energy Dashboard** | Developed for Sustainable Energy Management")
with footer_col2:
    st.markdown(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
