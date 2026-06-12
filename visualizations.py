import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import os

plt.style.use('dark_background')
plt.rcParams['figure.figsize'] = (12, 6)


def create_size_distribution_histogram(df, save_path='visualizations/size_distribution.png'):
    try:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.hist(df['diameter_km'], bins=30, color='steelblue', edgecolor='white', alpha=0.7)
        ax.set_xlabel('Diameter (km)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_title('Asteroid Size Distribution', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        os.makedirs('visualizations', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved: {save_path}")
        plt.show()
    except Exception as e:
        print(f"❌ Error: {e}")


def create_distance_vs_speed_scatter(df, save_path='visualizations/distance_vs_speed.html'):
    try:
        color_map = {'HAZARDOUS': 'red', 'MONITOR': 'orange', 'SAFE': 'green'}
        fig = go.Figure()
        
        for hazard_level in ['HAZARDOUS', 'MONITOR', 'SAFE']:
            mask = df['hazard_level'] == hazard_level
            subset = df[mask]
            fig.add_trace(go.Scatter(
                x=subset['distance_km'],
                y=subset['speed_kmh'],
                mode='markers',
                name=hazard_level,
                marker=dict(
                    size=subset['diameter_km'] * 5,
                    color=color_map[hazard_level],
                    opacity=0.7
                ),
                text=[f"{n}<br>Distance: {d:,.0f} km<br>Speed: {s:,.0f} km/h" 
                      for n, d, s in zip(subset['name'], subset['distance_km'], subset['speed_kmh'])],
                hovertemplate='%{text}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Distance vs. Speed',
            xaxis_title='Distance (km)',
            yaxis_title='Speed (km/h)',
            hovermode='closest',
            plot_bgcolor='rgba(0,0,0,0.1)',
            paper_bgcolor='rgba(20,20,20,1)',
            font=dict(color='white'),
            width=1000,
            height=600
        )
        
        os.makedirs('visualizations', exist_ok=True)
        fig.write_html(save_path)
        print(f"✅ Saved: {save_path}")
        fig.show()
        return fig
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def create_approach_timeline_bar(df, save_path='visualizations/approach_timeline.png'):
    try:
        daily_counts = df.groupby(df['date'].dt.date).size()
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(range(len(daily_counts)), daily_counts.values, color='steelblue', edgecolor='white', alpha=0.7)
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_title('Asteroids Per Day', fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(daily_counts)))
        ax.set_xticklabels(daily_counts.index, rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        os.makedirs('visualizations', exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved: {save_path}")
        plt.show()
    except Exception as e:
        print(f"❌ Error: {e}")


def create_hazard_level_pie(df, save_path='visualizations/hazard_pie.html'):
    try:
        hazard_counts = df['hazard_level'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=hazard_counts.index,
            values=hazard_counts.values,
            marker=dict(colors=['red', 'orange', 'green']),
            textinfo='label+percent'
        )])
        fig.update_layout(
            title='Hazard Level Distribution',
            plot_bgcolor='rgba(0,0,0,0.1)',
            paper_bgcolor='rgba(20,20,20,1)',
            font=dict(color='white'),
            width=800,
            height=600
        )
        os.makedirs('visualizations', exist_ok=True)
        fig.write_html(save_path)
        print(f"✅ Saved: {save_path}")
        fig.show()
        return fig
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def create_distance_trend_line(df, save_path='visualizations/distance_trend.html'):
    try:
        closest_per_day = df.groupby(df['date'].dt.date).apply(lambda x: x.loc[x['distance_km'].idxmin()])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=closest_per_day.index,
            y=closest_per_day['distance_km'],
            mode='lines+markers',
            name='Closest',
            line=dict(color='steelblue', width=3),
            marker=dict(size=10),
            fill='tozeroy'
        ))
        fig.add_hline(y=50000, line_dash='dash', line_color='red')
        fig.update_layout(
            title='Distance Trend',
            xaxis_title='Date',
            yaxis_title='Distance (km)',
            plot_bgcolor='rgba(0,0,0,0.1)',
            paper_bgcolor='rgba(20,20,20,1)',
            font=dict(color='white'),
            width=1000,
            height=600
        )
        os.makedirs('visualizations', exist_ok=True)
        fig.write_html(save_path)
        print(f"✅ Saved: {save_path}")
        fig.show()
        return fig
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def create_diameter_vs_distance_scatter(df, save_path='visualizations/diameter_vs_distance.html'):
    try:
        fig = px.scatter(df,
            x='diameter_km',
            y='distance_km',
            color='hazard_level',
            size='speed_kmh',
            hover_name='name',
            color_discrete_map={'HAZARDOUS': 'red', 'MONITOR': 'orange', 'SAFE': 'green'},
            title='Diameter vs. Distance'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0.1)',
            paper_bgcolor='rgba(20,20,20,1)',
            font=dict(color='white'),
            width=1000,
            height=600
        )
        os.makedirs('visualizations', exist_ok=True)
        fig.write_html(save_path)
        print(f"✅ Saved: {save_path}")
        fig.show()
        return fig
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def create_all_visualizations(df, output_dir='visualizations'):
    print("\n" + "=" * 70)
    print("Creating All Visualizations...")
    print("=" * 70)
    
    create_size_distribution_histogram(df)
    create_distance_vs_speed_scatter(df)
    create_approach_timeline_bar(df)
    create_hazard_level_pie(df)
    create_distance_trend_line(df)
    create_diameter_vs_distance_scatter(df)
    
    print("\n" + "=" * 70)
    print("✅ All visualizations created!")
    print("=" * 70)