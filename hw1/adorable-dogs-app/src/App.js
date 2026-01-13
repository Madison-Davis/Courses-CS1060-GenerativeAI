import React, { useEffect, useState, useMemo } from "react";
import "./App.css";

function App() {
  const [dogs, setDogs] = useState([]);
  const [likedDogs, setLikedDogs] = useState({});
  const [selectedArea, setSelectedArea] = useState("");

  const regions = useMemo(() => ["South", "Midwest", "New England", "Great Plains", "Northwest", "Southwest"], []);

  useEffect(() => {
    // Fetch data of random names using RandomUser API
    const fetchDogNames = async (count = 12) => {
      try {
        const response = await fetch(`https://randomuser.me/api/?results=${count}&inc=name`);
        const data = await response.json();
        return data.results.map(user => user.name.first);
      } catch (error) {
        console.error("Error fetching dog names:", error);
        return Array(count).fill("Dog");
      }
    };

    // Create profiles of dogs with data to display
    // Fetch data of dog images using Dog CEO API
    const fetchDogs = async (count = 12) => {
      try {
        const imagesRes = await fetch(`https://dog.ceo/api/breeds/image/random/${count}`);
        const imagesData = await imagesRes.json();
        const names = await fetchDogNames(count);

        const dogData = imagesData.message.map((img, index) => ({
          id: index,
          name: names[index],
          photo: img,
          region: regions[Math.floor(Math.random() * regions.length)] // Random region
        }));

        setDogs(dogData);
      } catch (error) {
        console.error(error);
      }
    };

    fetchDogs();
  }, [regions]);

  // Alter the Heart icon when a user goes to like a dog's profile
  const toggleLike = (id) => {
    setLikedDogs((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  // Filter dogs by selected area
  const filteredDogs = selectedArea
    ? dogs.filter((dog) => dog.region === selectedArea)
    : dogs;

  return (
    <div className="app-container">
      <div className="sidebar">
        <h2>Welcome!</h2>
        <p>Welcome to Doggies For Hearts!  Pick your favorite dogs shown to the right.</p>
      </div>

      <div className="main-content">
        <div className="banner">
          <h1>Doggies For Hearts</h1>
        </div>

        <div className="area-select">
          <label htmlFor="area">Select your area: </label>
          <select
            id="area"
            value={selectedArea}
            onChange={(e) => setSelectedArea(e.target.value)}
          >
            <option value="">All Areas</option>
            {regions.map((region) => (
              <option key={region} value={region}>
                {region}
              </option>
            ))}
          </select>
        </div>

        <hr />

        <div className="dog-grid">
          {filteredDogs.map((dog) => (
            <div key={dog.id} className="dog-card">
              <div className="dog-icon">
                <img
                  src={dog.photo}
                  alt={dog.name}
                  style={{ width: "50px", height: "50px", borderRadius: "50%" }}
                />
              </div>
              <div className="dog-info">
                <h3>{dog.name}</h3>
                <p>{dog.region}</p>
              </div>
              <button
                className={`heart-button ${likedDogs[dog.id] ? "liked" : ""}`}
                onClick={() => toggleLike(dog.id)}
              >
                ❤️
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
