import { useState } from 'react'
import axios from 'axios';
import './App.css'

const VALID_CITIES = [
  { label: 'New York, NY', value: 'New York' },
  { label: 'Boston, MA', value: 'Boston' },
  { label: 'Hartford, CT', value: 'Hartford' },
  { label: 'Philadelphia, PA', value: 'Philadelphia' },
  { label: 'Miami, FL', value: 'Miami' },
  { label: 'Atlanta, GA', value: 'Atlanta' },
  { label: 'Charlotte, NC', value: 'Charlotte' },
  { label: 'Baltimore, MD', value: 'Baltimore' }
];

interface WeatherData {
  weather: {
    city: string;
    temperature: number;
    weather_description: string;
    humidity: number;
    wind_speed: number;
    timestamp: string;
  };
  energy: {
    solar: {
      ac_annual: number;
      capacity_factor: number;
    };
  };
}

function App() {
  const [selectedCity, setSelectedCity] = useState('');
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_ENDPOINT = "https://4azrnnnf10.execute-api.us-east-1.amazonaws.com/dev/{proxy+}";

  const fetchData = async () => {
    if (!selectedCity) return;
    
    setLoading(true);
    setError(null);
    setWeatherData(null);

    try {
      const res = await axios.get(`${API_ENDPOINT}/weather`, {
        params: { city: selectedCity }
      });
      
      setWeatherData(res.data);
    } catch (err) {
      setError(axios.isAxiosError(err) 
        ? err.response?.data?.error || "An error occurred"
        : "Failed to fetch data");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-container">
      <h1>Clean Energy City Analyzer</h1>
      
      <div className="city-selector">
        <select
          value={selectedCity}
          onChange={(e) => setSelectedCity(e.target.value)}
          disabled={loading}
        >
          <option value="">Select an East Coast City</option>
          {VALID_CITIES.map(city => (
            <option key={city.value} value={city.value}>
              {city.label}
            </option>
          ))}
        </select>

        <button 
          onClick={fetchData} 
          disabled={!selectedCity || loading}
        >
          {loading ? "Analyzing..." : "Submit"}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {weatherData && (
        <div className="results-container">
          <div className="weather-card">
            <h2> 🌎 Weather in {weatherData.weather.city}:</h2>
            <div className="weather-details">
              <p>Temperature: {weatherData.weather.temperature}°F</p>
              <p>Conditions: {weatherData.weather.weather_description}</p>
              <p>Humidity: {weatherData.weather.humidity}%</p>
              <p>Wind Speed: {weatherData.weather.wind_speed} mph</p>
              <p>Last Updated: {new Date(weatherData.weather.timestamp).toLocaleString()}</p>
            </div>
          </div>

          <div className="energy-card">
            <h2>☀️Solar Potential:</h2>
            <div className="energy-details">
              <div className="solar-stats">
                <p>Annual Output: {weatherData.energy.solar.ac_annual.toFixed(0)} kWh</p>
                <p>Capacity Factor: {(weatherData.energy.solar.capacity_factor * 100).toFixed(1)}%</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
