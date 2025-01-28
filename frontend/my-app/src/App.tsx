import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import axios from 'axios';
import './App.css'

function App() {
  const [city, setCity] = useState('');
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  // const [count, setCount] = useState(0)

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
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Enter a city: </h1>
      <input
        type = "text"
        value = {city}
        onChange = {(e) => setCity(e.target.value)}
        placeholder = "Enter city"
      />
      <div className="card">
        <button onClick={fetchData} disabled = {loading}>
          {loading ? "Loading...": "Get Weather Data"}
        </button>
        {error && <p style={{ color: "red"}}>{error}</p>}
        {weatherData && (
          <div>
            <p>Weather: {weatherData['weather_description']}</p>
            <p>Temperature: {weatherData['temperature']}°F</p>
          </div>
        )}
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
