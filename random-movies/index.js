const express = require('express');
const axios = require('axios');
require('dotenv').config();

const app = express();

const PORT = process.env.PORT || 3000;
const URL_MOVIES = process.env.URL_MOVIES;

app.get("/randommovies", async (req, res) => {
  try {
    const { limit } = req.query;
    const parsedLimit = parseInt(limit, 10);

    const response = await axios.get(URL_MOVIES + `/movies/random?limit=${parsedLimit}`);
    const movies = response.data;

    res.json(movies);
  } catch (error) {
    console.error("Error fetching random movies:", error);
    res.status(500).json({ message: "Error fetching random movies" });
  }
});

app.listen(PORT, () => {
  console.log(`RandomMovies service listening on http://localhost:${PORT}`);
});