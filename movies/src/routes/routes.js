const express = require('express');
const Movie = require('../model/database');

const router = express.Router();

router.get('/random', async (req, res) => {    
    try {
        const {limit} = req.query;
        const parsedLimit = parseInt(limit, 10);

        if (isNaN(parsedLimit) || parsedLimit <= 0) {
            return res.status(400).send('Invalid limit parameter');
        }

        const movies = await Movie.getRandomMovies(parsedLimit);
        res.json(movies);
    } catch (error) {
        res.status(500).send('Error fetching movies');
    }
});

router.get('/', async (req, res) => {
    try {
        const {id} = req.query;
        
        if (!id) {
            return res.status(400).send('Invalid id parameter');
        }

        const movie = await Movie.getMovieById(id);
        res.json(movie);
    } catch (error) {
        res.status(500).send('Error fetching movies');
    }
});

router.post('/title', async (req, res) => {
    try {
        const { title } = req.body;

        if (!title) {
            return res.status(400).send('Invalid title parameter');
        }

        const movies = await Movie.getMovieByTitle(title);
        res.json(movies);
    } catch (error) {
        res.status(500).send('Error fetching movies');
    }
});

router.post('/director', async (req, res) => {
    try {
        const {director} = req.body;

        if (!director) {
            return res.status(400).send('Invalid director parameter');
        }

        const movies = await Movie.getMovieByDirector(req.query.director);
        res.json(movies);
    } catch (error) {
        res.status(500).send('Error fetching movies');
    }
});

router.post('/filter', async (req, res) => {
    try {
        const filter = req.body;
        const {limit} = req.query;
        const parsedLimit = parseInt(limit, 10);

        if (!filter) {
            return res.status(400).send('Invalid filter parameter');
        }

        const movies = await Movie.getMoviesByFilter(filter, parsedLimit);
        res.json(movies);
    } catch (error) {
        res.status(500).send('Error fetching movies');
    }
});

router.post('/search', async (req, res) => {
    try {
        const { text, limit } = req.body;
        if (!text) return res.status(400).send('Invalid text parameter');
        if (!limit) return res.status(400).send('Invalid limit parameter');
        const movies = await Movie.getMoviesByText(text, limit);
        res.json(movies);
    } catch (error) {
        res.status(500).send('Error fetching movies');
    }
});

module.exports = router;