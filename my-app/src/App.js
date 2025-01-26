import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';

function App() {
  const mapContainerRef = useRef(null);
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
      style: 'mapbox://styles/mapbox/dark-v10',
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

      // Existing heatmap layer
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
            1, 'rgba(178,24,43,0.6)'
          ],
          'heatmap-radius': 40,
          'heatmap-opacity': 0.7,
        },
      });

      // New vertical beam layer
      map.addLayer({
        id: 'city-beams',
        type: 'circle',
        source: 'cities',
        paint: {
          'circle-radius': [
            'interpolate', 
            ['linear'], 
            ['get', 'kWh'], 
            0, 10,  // Smaller radius for low kWh
            1000, 50  // Larger radius for high kWh
          ],
          'circle-color': [
            'interpolate',
            ['linear'],
            ['get', 'kWh'],
            0, 'rgba(0,255,0,0.1)',     // Green for low energy
            500, 'rgba(255,255,0,0.3)', // Yellow for medium energy
            1000, 'rgba(255,0,0,0.5)'   // Red for high energy
          ],
          'circle-translate-vertical': [
            'interpolate', 
            ['exponential', 1.5], 
            ['zoom'], 
            4, 200,   // More vertical stretch at lower zoom levels
            10, 500   // Even more vertical stretch at higher zoom levels
          ],
          'circle-translate': [0, 0],
          'circle-opacity': 0.7,
          'circle-blur': 0.7,
        },
      });

      // Existing city points layer
      map.addLayer({
        id: 'city-points',
        type: 'circle',
        source: 'cities',
        paint: {
          'circle-radius': 6,
          'circle-color': 'white',
          'circle-stroke-color': 'black',
          'circle-stroke-width': 1,
        },
      });

      // Existing popup and cursor interaction
      map.on('click', 'city-points', (e) => {
        const { city, kWh } = e.features[0].properties;
        new mapboxgl.Popup()
          .setLngLat(e.lngLat)
          .setHTML(`<strong>${city}</strong><br>Energy Forecast: ${kWh.toFixed(2)} kWh`)
          .addTo(map);
      });

      map.on('mouseenter', 'city-points', () => {
        map.getCanvas().style.cursor = 'pointer';
      });

      map.on('mouseleave', 'city-points', () => {
        map.getCanvas().style.cursor = '';
      });
    });

    return () => map.remove();
  }, [mapboxAccessToken, dummyData]);

  // Rest of the component remains the same
  const handleDateChange = (event) => {
    setSelectedDate(event.target.value);
  };

  const today = new Date().toISOString().slice(0, 10);
  const twoWeeksLater = new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);

  return (
    <div className="App h-screen w-screen overflow-hidden relative">
      <div ref={mapContainerRef} className="map-container h-full w-full" />
      <div className="absolute top-6 left-6 z-10">
        <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-2xl border border-gray-200 p-6 w-96 transform transition-all hover:scale-[1.03] hover:shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-blue-600">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              <h3 className="text-lg font-semibold text-gray-800">Select a Date</h3>
            </div>
          </div>

          <input
            type="date"
            value={selectedDate}
            onChange={handleDateChange}
            className="
              w-full p-3 
              border border-gray-300 rounded-lg 
              focus:ring-2 focus:ring-blue-500 focus:border-transparent
              text-gray-700 
              transition duration-300
              cursor-pointer
              appearance-none
              hover:border-blue-400
            "
            min={today}
            max={twoWeeksLater}
          />

          <div className="text-sm text-gray-500 mt-3 text-center">
            Choose a date within the next 14 days.
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;