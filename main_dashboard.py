import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from data_fetchers import fetch_asteroids
from data_processors import process_asteroids, get_summary_stats, get_hazardous_asteroids

st.set_page_config(
    page_title="🚀 NASA Asteroid Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    st.sidebar.title("⚙️ Configuration")
    st.sidebar.markdown("---")
    
    days_ahead = st.sidebar.slider(
        "Days to Check",
        min_value=1,
        max_value=7,
        value=7,
        help="How many days ahead to fetch asteroid data"
    )
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "📊 **NASA Asteroid Dashboard**\n\n"
        "Real-time visualization of near-Earth asteroids using NASA's free APIs.\n\n"
        "**Data Source:** NASA NEO API\n"
        "**Updated:** Live\n"
        "**Purpose:** Track potentially hazardous asteroids"
    )

    st.title("🚀 NASA Asteroid Dashboard")
    st.markdown("Real-time Near-Earth Asteroid Monitoring System")
    st.markdown("---")

    with st.spinner("🔄 Fetching asteroid data from NASA API..."):
        raw_data = fetch_asteroids(days_ahead=days_ahead)
    
    if raw_data is None:
        st.error("❌ Failed to fetch data from NASA API. Please check your API key.")
        return
    
    with st.spinner("⚙️ Processing data with Pandas..."):
        df = process_asteroids(raw_data)
    
    if df is None:
        st.error("❌ Failed to process asteroid data.")
        return
    
    st.success("✅ Data loaded successfully!")

    stats = get_summary_stats(df)
    hazardous = get_hazardous_asteroids(df)
  
    st.markdown("## 📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔢 Total Asteroids", f"{stats['total_count']}")
    
    with col2:
        st.metric("🔴 Hazardous", f"{stats['hazardous_count']}", f"{(stats['hazardous_count']/stats['total_count']*100):.1f}%")
    
    with col3:
        st.metric("📍 Closest Approach", f"{stats['closest_approach_km']:,.0f} km")
    
    with col4:
        st.metric("⚡ Fastest Speed", f"{stats['fastest_speed_kmh']:,.0f} km/h")
    
    st.markdown("---")
 
    if stats['hazardous_count'] > 0:
        st.warning(f"⚠️ **{stats['hazardous_count']} HAZARDOUS ASTEROID(S) DETECTED!**")
        
        with st.expander("👁️ View Hazardous Asteroids (NASA Classification)", expanded=True):
            # Filter by NASA's classification
            nasa_hazardous = df[df['is_hazardous'] == True].copy()
            
            if len(nasa_hazardous) > 0:
                hazardous_display = nasa_hazardous[['name', 'date', 'diameter_km', 'distance_km', 'speed_kmh']].reset_index(drop=True)
                hazardous_display.columns = ['Name', 'Date', 'Diameter (km)', 'Distance (km)', 'Speed (km/h)']
                st.dataframe(hazardous_display, width='stretch', hide_index=True)
            else:
                st.info("ℹ️ No hazardous asteroids in current data")
    else:
        st.success(f"✅ No hazardous asteroids detected in the next {days_ahead} days")
    
    st.markdown("---")

    st.markdown("## 📈 Visualizations")
    
    col1, col2 = st.columns(2)
   
    with col1:
        st.subheader("Asteroid Size Distribution")
        try:
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=df['diameter_km'],
                nbinsx=30,
                name='Asteroids',
                marker_color='steelblue'
            ))
            fig_hist.update_layout(
                xaxis_title="Diameter (km)",
                yaxis_title="Count",
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0.1)',
                paper_bgcolor='rgba(20,20,20,1)',
                font=dict(color='white'),
                height=400
            )
            st.plotly_chart(fig_hist, width='stretch')
        except Exception as e:
            st.error(f"Error creating histogram: {e}")
    
    with col2:
        st.subheader("Hazard Level Distribution")
        try:
            hazard_counts = df['hazard_level'].value_counts()
            fig_pie = go.Figure(data=[go.Pie(
                labels=hazard_counts.index,
                values=hazard_counts.values,
                marker=dict(colors=['red', 'orange', 'green']),
                textinfo='label+percent+value'
            )])
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0.1)',
                paper_bgcolor='rgba(20,20,20,1)',
                font=dict(color='white'),
                height=400
            )
            st.plotly_chart(fig_pie, width='stretch')
        except Exception as e:
            st.error(f"Error creating pie chart: {e}")
   
    col1, col2 = st.columns(2)
   
    with col1:
        st.subheader("Distance vs. Speed")
        try:
            color_map = {'HAZARDOUS': 'red', 'MONITOR': 'orange', 'SAFE': 'green'}
            fig_scatter = go.Figure()
            
            for hazard_level in ['HAZARDOUS', 'MONITOR', 'SAFE']:
                mask = df['hazard_level'] == hazard_level
                subset = df[mask]
                fig_scatter.add_trace(go.Scatter(
                    x=subset['distance_km'],
                    y=subset['speed_kmh'],
                    mode='markers',
                    name=hazard_level,
                    marker=dict(
                        size=subset['diameter_km'] * 3,
                        color=color_map[hazard_level],
                        opacity=0.7
                    ),
                    text=[f"{n}<br>Dist: {d:,.0f} km<br>Speed: {s:,.0f} km/h" 
                          for n, d, s in zip(subset['name'], subset['distance_km'], subset['speed_kmh'])],
                    hovertemplate='%{text}<extra></extra>'
                ))
            
            fig_scatter.update_layout(
                xaxis_title="Distance (km)",
                yaxis_title="Speed (km/h)",
                hovermode='closest',
                plot_bgcolor='rgba(0,0,0,0.1)',
                paper_bgcolor='rgba(20,20,20,1)',
                font=dict(color='white'),
                height=400
            )
            st.plotly_chart(fig_scatter, width='stretch')
        except Exception as e:
            st.error(f"Error creating scatter plot: {e}")

    with col2:
        st.subheader("Asteroids per Day")
        try:
            daily_counts = df.groupby(df['date'].dt.date).size()
            fig_timeline = go.Figure()
            fig_timeline.add_trace(go.Bar(
                x=daily_counts.index,
                y=daily_counts.values,
                marker_color='steelblue',
                text=daily_counts.values,
                textposition='auto'
            ))
            fig_timeline.update_layout(
                xaxis_title="Date",
                yaxis_title="Count",
                plot_bgcolor='rgba(0,0,0,0.1)',
                paper_bgcolor='rgba(20,20,20,1)',
                font=dict(color='white'),
                height=400
            )
            st.plotly_chart(fig_timeline, width='stretch')
        except Exception as e:
            st.error(f"Error creating timeline: {e}")
    
    st.markdown("---")

    st.markdown("## 📋 Detailed Data")
    st.subheader("All Asteroids")
    
    col1, col2 = st.columns(2)
    
    with col1:
        filter_hazard = st.multiselect(
            "Filter by Hazard Level",
            options=['HAZARDOUS', 'MONITOR', 'SAFE'],
            default=['HAZARDOUS', 'MONITOR', 'SAFE']
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            options=['Distance (Closest First)', 'Speed (Fastest First)', 'Diameter (Largest First)'],
            index=0
        )
  
    filtered_df = df[df['hazard_level'].isin(filter_hazard)].copy()
    
    if sort_by == 'Distance (Closest First)':
        filtered_df = filtered_df.sort_values('distance_km')
    elif sort_by == 'Speed (Fastest First)':
        filtered_df = filtered_df.sort_values('speed_kmh', ascending=False)
    else:
        filtered_df = filtered_df.sort_values('diameter_km', ascending=False)
 
    display_df = filtered_df[['name', 'date', 'diameter_km', 'distance_km', 'speed_kmh', 'hazard_level']].copy()
    display_df = display_df.reset_index(drop=True)
    display_df.columns = ['Name', 'Date', 'Diameter (km)', 'Distance (km)', 'Speed (km/h)', 'Hazard']
    
    st.dataframe(display_df, width='stretch', height=400, hide_index=True)
    
    st.markdown("---")
  
    st.markdown("## 📊 Statistical Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Diameter", f"{stats['average_diameter_km']:.2f} km")
    with col2:
        st.metric("Average Speed", f"{stats['average_speed_kmh']:.0f} km/h")
    with col3:
        st.metric("Distance Range", f"{stats['closest_approach_km']:,.0f} km")
   
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
        <p>🚀 NASA Asteroid Dashboard | Real-time Data from NASA NEO API</p>
        <p>Last Updated: Live | Data Refreshes on Demand</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()