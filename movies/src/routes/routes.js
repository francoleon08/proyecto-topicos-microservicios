const express = require('express');
const Movie = require('../model/database');

const router = express.Router();

router.get('/', async (req, res) => {
    

    try {
        const movies = await Movie.getRandomMovies(1);
        res.json(movies);
    } catch (error) {
        res.status(500).send('Error fetching movies');
    }
});

module.exports = router;