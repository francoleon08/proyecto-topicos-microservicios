const Realm = require("realm-web");
const {getFromCache, cacheResult} = require('../cache/redisClient');
require('dotenv').config();

const MONGODB_APP_ID = process.env.MONGODB_APP_ID;

const app = new Realm.App({ id: MONGODB_APP_ID });

async function getAuthenticatedUser() {
    const credentials = Realm.Credentials.anonymous();
    try {
        const user = await app.logIn(credentials);
        return user || null;
    } catch (err) {
        console.error("Error de autenticación anónima:", err);
        return null;
    }
}

async function getRandomMovies(n) {
    const user = await getAuthenticatedUser();
    if (!user) return [];
    
    try {
        return await user.functions.get_n_randoms_movies(n);
    } catch (err) {
        console.error("Error al obtener películas aleatorias:", err);
        return [];
    }
}

async function getMovieByTitle(title) {
    const cachedMovie = await getFromCache(title);
    if (cachedMovie) return cachedMovie;
    
    const user = await getAuthenticatedUser();
    if (!user) return null;

    try {
        const movie = await user.functions.get_movie_by_title(title);
        await cacheResult(title, movie);
        return movie;
    } catch (err) {
        console.error("Error al obtener película por título:", err);
        return null;
    }
}

async function getMovieByDirector(director) {
    const cachedMovies = await getFromCache(director);
    if (cachedMovies) return cachedMovies;
    
    const user = await getAuthenticatedUser();
    if (!user) return [];
    
    try {
        const movies = await user.functions.get_movie_by_director(director);
        await cacheResult(director, movies);
        return movies;
    } catch (err) {
        console.error("Error al obtener películas por director:", err);
        return [];
    }
}

module.exports = { getRandomMovies, getMovieByTitle, getMovieByDirector };
