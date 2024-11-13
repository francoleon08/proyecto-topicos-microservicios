const express = require('express');
const axios = require('axios');
const app = express();
const cors = require('cors'); 
const PORT = 3001; // Port for RandomMovies service

//app.use(cors({ origin: "http://localhost:3000" })); // Allow only from your frontend

// Get N random movies (e.g., 6 random movies)
app.get("/randommovies", async (req, res) => {
    try {
      const M = 10; // Number of random movies to fetch
      const N = 6; // Number of random movies needed for the frontend
      const response = await axios.get(`http://movies:3000/movies/random?limit=${M}`); // Request N movies from the 'Movies' service
      const movies = response.data;
  
      // Get N random movies
      const randomMovies = [];
      for (let i = 0; i < N; i++) {
        randomMovies.push(movies[i]);
      }
  
      res.json(randomMovies); // Send the random movies back to the client
    } catch (error) {
      console.error("Error fetching random movies:", error);
      res.status(500).json({ message: "Error fetching random movies" });
    }
  });
  
  app.listen(PORT, () => {
    console.log(`RandomMovies service listening on http://localhost:${PORT}`);
  });