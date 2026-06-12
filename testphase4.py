from data_fetchers import fetch_asteroids
from data_processors import (
    process_asteroids,
    get_summary_stats,
    get_hazardous_asteroids,
    get_asteroids_by_date,
    print_asteroid_summary
)
import pandas as pd


def test_phase4():
    
    print("=" * 70)
    print("🧪 PHASE 4: Data Processing with Pandas")
    print("=" * 70)
    
    print("\n[STEP 1] Fetching asteroid data from NASA API...")
    print("-" * 70)
    
    raw_data = fetch_asteroids(days_ahead=7)
    
    if raw_data is None:
        print("❌ Failed to fetch data")
        return False
    
    print("\n[STEP 2] Processing data with Pandas...")
    print("-" * 70)
    
    df = process_asteroids(raw_data)
    
    if df is None:
        print("❌ Failed to process data")
        return False
    
    print("\n[STEP 3] DataFrame Structure")
    print("-" * 70)
    
    print(f"\n📋 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\n📊 Data Types:")
    print(df.dtypes)
    
    print(f"\n👀 First 5 asteroids:")
    print(df.head())
    
    print("\n[STEP 4] Summary Statistics")
    print("-" * 70)
    
    stats = get_summary_stats(df)
    
    if stats:
        print_asteroid_summary(df)
    
    print("\n[STEP 5] Hazardous Asteroids")
    print("-" * 70)
    
    hazardous = get_hazardous_asteroids(df)
    
    if len(hazardous) > 0:
        print(f"\n🔴 Found {len(hazardous)} HAZARDOUS asteroid(s):\n")
        for idx, row in hazardous.iterrows():
            print(f"   • {row['name']}")
            print(f"     Distance: {row['distance_km']:.2f} km ({row['distance_miles']:.2f} miles)")
            print(f"     Diameter: {row['diameter_km']:.2f} km")
            print(f"     Speed: {row['speed_kmh']:.2f} km/h")
            print()
    else:
        print("\n✅ No hazardous asteroids detected!")
    
    print("\n[STEP 6] Asteroids by Date")
    print("-" * 70)
    
    by_date = get_asteroids_by_date(df)
    
    print("\n📅 Breakdown by date:")
    for date, group in by_date.items():
        closest = group['distance_km'].min()
        count = len(group)
        print(f"   {date}: {count} asteroids (closest: {closest:.2f} km)")
    
    print("\n[STEP 7] Pandas Operations Demo")
    print("-" * 70)
    
    print("\n1️⃣  Asteroids larger than 1 km:")
    large = df[df['diameter_km'] > 1.0]
    print(f"   Found {len(large)} asteroids")
    if len(large) > 0:
        print(large[['name', 'diameter_km', 'distance_km']].head(3))
    
    print("\n2️⃣  Fastest approaching asteroids:")
    fastest = df.nlargest(3, 'speed_kmh')
    print(fastest[['name', 'speed_kmh', 'distance_km']])
    
    print("\n3️⃣  Average distance by hazard level:")
    avg_distance = df.groupby('hazard_level')['distance_km'].mean()
    print(avg_distance)
    
    print("\n4️⃣  Data description (statistics):")
    print(df.describe())

    print("\n[STEP 8] Saving processed data...")
    print("-" * 70)
    
    try:
        df.to_csv('data/asteroids_processed.csv', index=False)
        print("✅ Saved to data/asteroids_processed.csv")
    except Exception as e:
        print(f"⚠️  Could not save CSV: {e}")

    print("\n[STEP 9] Summary")
    print("-" * 70)
    print("\n✅ Phase 4 Complete!")
    print("\nYou learned:")
    print("   • Converting JSON to Pandas DataFrames")
    print("   • Extracting and cleaning data")
    print("   • Creating new calculated columns")
    print("   • Filtering and grouping data")
    print("   • Getting summary statistics")
    print("   • Saving data to CSV")
    
    print("\n📊 DataFrame is ready for Phase 5: Visualization!")
    
    return True


if __name__ == "__main__":
    try:
        success = test_phase4()
        
        if success:
            print("\n" + "=" * 70)
            print("🚀 Next Step: Phase 5 - Create Visualizations with Matplotlib/Plotly!")
            print("=" * 70)
        else:
            print("\n" + "=" * 70)
            print("⚠️  Phase 4 test failed. Please fix the issues above.")
            print("=" * 70)
    
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\nMake sure you have:")
        print("   • pandas installed: pip install pandas")
        print("   • data_fetchers.py in the same folder")
        print("   • data_processors.py in the same folder")
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()