import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';

function App() {
  const mapContainerRef = useRef(null);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().slice(0, 10));
  const mapboxAccessToken = "api token";

  useEffect(() => {
    mapboxgl.accessToken = mapboxAccessToken;
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [-74.5, 40],
      zoom: 9,
    });

    map.addControl(new mapboxgl.NavigationControl(), 'top-right');
    return () => map.remove();
  }, [mapboxAccessToken]);

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
