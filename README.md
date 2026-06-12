# 🚀 NASA Asteroid Dashboard

A real-time interactive dashboard that monitors near-Earth asteroids using NASA's free APIs. Built with Python, Pandas, Plotly, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📊 Features

✨ **Real-Time Data**
- Live asteroid data from NASA's Near-Earth Object API
- Automatic hazard detection and classification
- Updates on demand with just one click

📈 **Interactive Visualizations**
- Asteroid size distribution histogram
- Hazard level pie chart
- Distance vs. speed scatter plot (bubble size = diameter)
- Daily approach timeline

⚠️ **Hazard Alert System**
- Detects potentially hazardous asteroids
- Color-coded risk levels (Red/Orange/Green)
- Detailed asteroid information table

📋 **Advanced Data Analysis**
- Filterable and sortable data table
- Statistical summaries
- Multiple sorting options (distance, speed, diameter)
- Metrics display (total count, average speeds, distance range)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.8+ |
| **Data Fetching** | Requests + NASA APIs |
| **Data Processing** | Pandas |
| **Visualizations** | Plotly + Matplotlib |
| **Dashboard** | Streamlit |
| **API** | NASA NEO (Near-Earth Object) API |

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/nasa-dashboard.git
cd nasa-dashboard
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Get NASA API Key
1. Go to https://api.nasa.gov
2. Fill in the form (email, name)
3. Get your API key instantly via email

### Step 5: Create .env File
Create a `.env` file in the project root:
```
NASA_API_KEY=your_actual_api_key_here
```

**Important:** Never commit `.env` to GitHub! It's already in `.gitignore`

---

## 🚀 Running the Dashboard

```bash
streamlit run main_dashboard.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
nasa-dashboard/
├── config.py                    # API configuration & endpoints
├── .env                         # API key (DO NOT COMMIT)
├── data_fetchers.py            # Fetch data from NASA APIs
├── data_processors.py          # Process & analyze data with Pandas
├── visualizations.py           # Create charts with Matplotlib & Plotly
├── main_dashboard.py           # Main Streamlit dashboard
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
├── README.md                   # This file
├── test.py                     # Basic API test
├── test_phase4.py              # Data processing test
├── test_phase5.py              # Visualization test
├── visualizations/             # Generated chart files (PNG/HTML)
└── data/                       # Cached data files
```

---

## 🧪 Testing

### Test API Connection
```bash
python test.py
```

### Test Data Processing
```bash
python test_phase4.py
```

### Test Visualizations
```bash
python test_phase5.py
```

---

## 📊 Dashboard Features Explained

### Key Metrics Section
- **Total Asteroids**: Count of asteroids in the selected time period
- **Hazardous**: Number and percentage of NASA-designated hazardous asteroids
- **Closest Approach**: Minimum distance from Earth
- **Fastest Speed**: Maximum relative velocity

### Visualizations
1. **Size Distribution**: Shows how many asteroids of each size are approaching
2. **Hazard Levels**: Pie chart of SAFE/MONITOR/HAZARDOUS breakdown
3. **Distance vs Speed**: Interactive scatter showing relationship between distance and velocity
4. **Daily Timeline**: Bar chart showing asteroids per day

### Data Table
- Filter by hazard level (HAZARDOUS, MONITOR, SAFE)
- Sort by distance, speed, or diameter
- View all asteroid details including diameter, distance, and speed

---

## 🔄 Data Flow

```
NASA APIs
    ↓
fetch_asteroids() ──→ Raw JSON data
    ↓
process_asteroids() ──→ Pandas DataFrame
    ↓
Visualizations & Dashboard ──→ Interactive UI
```

---

## 📡 NASA APIs Used

### Near-Earth Object (NEO) API
- **Endpoint**: `/neo/rest/v1/feed`
- **Data**: Asteroid name, diameter, distance, speed, hazard classification
- **Frequency**: Real-time
- **Rate Limit**: 50,000 requests/day (DEMO_KEY: 30/hour)

---

## 🎨 Customization

### Change Days Ahead
Edit `config.py`:
```python
DEFAULT_DAYS_AHEAD = 7  # Change to 1-7
```

### Adjust Hazard Thresholds
Edit `config.py`:
```python
HAZARD_THRESHOLD_KM = 0.05  # 50,000 km
```

### Modify Dashboard Layout
Edit `main_dashboard.py` to add/remove sections, change colors, add widgets, etc.

---

## 🚀 Deployment

### Deploy to Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. Dashboard is live! 🎉

### Deploy to Heroku/AWS/GCP
See Streamlit deployment documentation for advanced options.

---

## 📈 Performance

- **Data Fetch**: ~2-3 seconds
- **Data Processing**: ~1 second
- **Dashboard Load**: ~3-5 seconds
- **Chart Rendering**: <1 second (Streamlit caching)

---

## 🐛 Troubleshooting

### API Key Errors
- Verify key in `.env` file
- Check at https://api.nasa.gov
- Ensure no extra spaces in `.env`

### Dashboard Not Loading
- Check Python version: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`
- Clear Streamlit cache: `streamlit cache clear`

### Charts Not Showing
- Verify Plotly installed: `pip install plotly`
- Check internet connection
- Try refreshing the browser

---

## 📚 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NASA API Documentation](https://api.nasa.gov/)
- [Requests Library](https://requests.readthedocs.io/)

---

## 🎓 Project Highlights

This project demonstrates:
- ✅ API integration and HTTP requests
- ✅ JSON parsing and data transformation
- ✅ Data cleaning and processing with Pandas
- ✅ Statistical analysis and calculations
- ✅ Data visualization (static & interactive)
- ✅ Web dashboard development
- ✅ Python best practices and project organization
- ✅ Error handling and debugging
- ✅ Git version control

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 👤 Author

Built with ❤️ using Python, NASA APIs, and Streamlit

---

## 🌟 Future Enhancements

- [ ] Add real-time updates with WebSocket
- [ ] Cache data for faster loading
- [ ] Export reports as PDF
- [ ] Add more NASA APIs (Solar Flares, ISS Position, etc.)
- [ ] Machine learning predictions for asteroid paths
- [ ] Mobile-responsive design
- [ ] User authentication
- [ ] Historical data tracking

---

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments
3. Check NASA API documentation
4. Open an issue on GitHub

---

**Happy tracking! 🚀🌍**
