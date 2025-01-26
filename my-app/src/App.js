import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';

function App() {
  const mapContainerRef = useRef(null);
  const [mapStyle, setMapStyle] = useState('mapbox://styles/mapbox/dark-v11'); // Default to dark mode
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().slice(0, 10));
  const mapboxAccessToken = "pk.eyJ1IjoiYnJvcGVyc29uMSIsImEiOiJjbTZjaWJjcGEwaWpzMmxvb2NqbGk4bW5zIn0.1SxGezdKuvQb7tvOcVeKJg"; // Replace with your actual Mapbox token

  const dummyData = [
    { city: "New York", coordinates: [-74.006, 40.7128], kWh: Math.random() * 1000 },
    { city: "Los Angeles", coordinates: [-118.2437, 34.0522], kWh: Math.random() * 1000 },
    { city: "Chicago", coordinates: [-87.6298, 41.8781], kWh: Math.random() * 1000 },
    { city: "Houston", coordinates: [-95.3698, 29.7604], kWh: Math.random() * 1000 },
    { city: "Miami", coordinates: [-80.1918, 25.7617], kWh: Math.random() * 1000 },
  ];

  useEffect(() => {
    mapboxgl.accessToken = mapboxAccessToken;
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: mapStyle,
      center: [-98.5795, 39.8283], // Center of the USA
      zoom: 4,
    });

    map.on('load', () => {
      map.addSource('cities', {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: dummyData.map((city) => ({
            type: 'Feature',
            geometry: {
              type: 'Point',
              coordinates: city.coordinates,
            },
            properties: {
              city: city.city,
              kWh: city.kWh,
            },
          })),
        },
      });

      map.addLayer({
        id: 'heatmap',
        type: 'heatmap',
        source: 'cities',
        paint: {
          'heatmap-weight': ['interpolate', ['linear'], ['get', 'kWh'], 0, 0, 1000, 1],
          'heatmap-intensity': 1,
          'heatmap-color': [
            'interpolate',
            ['linear'],
            ['heatmap-density'],
            0, 'rgba(0,0,0,0)',
            0.2, 'rgba(103,169,207,0.6)',
            0.4, 'rgba(209,229,240,0.6)',
            0.6, 'rgba(253,219,199,0.6)',
            0.8, 'rgba(239,138,98,0.6)',
            1, 'rgba(178,24,43,0.6)',
          ],
          'heatmap-radius': 40,
          'heatmap-opacity': 0.7,
        },
      });
    });

    return () => map.remove();
  }, [mapStyle, mapboxAccessToken, dummyData]);

  const handleStyleToggle = () => {
    setMapStyle((prevStyle) =>
      prevStyle === 'mapbox://styles/mapbox/dark-v11'
        ? 'mapbox://styles/mapbox/outdoors-v12'
        : 'mapbox://styles/mapbox/dark-v11'
    );
  };

  const handleDateChange = (event) => {
    setSelectedDate(event.target.value);
  };

  const today = new Date().toISOString().slice(0, 10);
  const twoWeeksLater = new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);

  return (
    <div className="App h-screen w-screen overflow-hidden relative">
      <div ref={mapContainerRef} className="map-container h-full w-full" />
      <div className="absolute top-6 left-6 z-10 space-y-4">
        <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-2xl border border-gray-200 p-6 w-96 transform transition-all hover:scale-[1.03] hover:shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Select a Date</h3>
          </div>

          <input
            type="date"
            value={selectedDate}
            onChange={handleDateChange}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-700 transition duration-300 cursor-pointer hover:border-blue-400"
            min={today}
            max={twoWeeksLater}
          />

          <div className="text-sm text-gray-500 mt-3 text-center">
            Choose a date within the next 14 days.
          </div>
        </div>
      </div>
      <div className="absolute top-6 right-6 z-10">
        <button
          onClick={handleStyleToggle}
          className="bg-white text-gray-800 px-4 py-2 rounded-lg shadow-md hover:bg-gray-100 transition"
        >
          Toggle Mode
        </button>
      </div>
    </div>
  );
}

export default App;
