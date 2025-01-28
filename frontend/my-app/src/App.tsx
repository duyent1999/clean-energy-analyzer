import { useState } from 'react'
import axios from 'axios';
import './App.css'

function App() {
  const [city, setCity] = useState('');
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async() => {

    setLoading(true);
    setError(null); 

    try {
      const res = await axios.get("https://z3tjzv0tw6.execute-api.us-east-1.amazonaws.com/dev/weather", {params: {city: city}});
      setWeatherData(res.data);
    } catch (err) {
      setError("Error fetching weather data");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <h1>Enter a city: </h1>
      <input
        type = "text"
        value = {city}
        onChange = {(e) => setCity(e.target.value)}
        placeholder = "Enter city name"
      />
      <div className="card">
        <button onClick={fetchData} disabled = {loading}>
          {loading ? "Loading...": "Get Weather Data"}
        </button>
        {error && <p style={{ color: "red"}}>{error}</p>}
        {weatherData && (
        <div style={{ border: "1px solid #ddd", padding: "20px", borderRadius: "8px" }}>
          <h2>Weather in {city} {weatherData.city}</h2>
          <p>Temperature: {weatherData.temperature}°C</p>
          <p>Weather: {weatherData.weather_description}</p>
          <p>Humidity: {weatherData.humidity}%</p>
          <p>Wind Speed: {weatherData.wind_speed} m/s</p>
          <p>Last Updated: {weatherData.timestamp}</p>
        </div>
        )}
      </div>
    </>
  )
}

export default App
