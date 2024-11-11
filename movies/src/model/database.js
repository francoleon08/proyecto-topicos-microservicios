const Realm = require("realm-web");
require('dotenv').config();

id_mongo = process.env.MONGODB_APP_ID;

const app = new Realm.App({ id: id_mongo });

async function getRandomMovies(n) {        
    const credentials = Realm.Credentials.anonymous();

    try {        
        const user = await app.logIn(credentials);

        if (!user) {
            console.error("Failed to log in as an anonymous user.");
            return [];
        }
    
        const result = await user.functions.get_n_randoms_movies(n);
                
        return result;
    } catch (err) {
        console.error("Failed to log in as an anonymous user.", err);
        return [];
    }
}

async function getMovieByTitle(title) {
    const credentials = Realm.Credentials.anonymous();

    try {
        const user = await app.logIn(credentials);

        if (!user) {
            console.error("Failed to log in as an anonymous user.");
            return [];
        }

        const result = await user.functions.get_movie_by_title(title);

        return result;
    } catch (err) {
        console.error("Failed to log in as an anonymous user.", err);
        return [];
    }
}

async function getMovieByDirector(director) {
    const credentials = Realm.Credentials.anonymous();

    try {
        const user = await app.logIn(credentials);

        if (!user) {
            console.error("Failed to log in as an anonymous user.");
            return [];
        }

        const result = await user.functions.get_movie_by_director(director);

        return result;
    } catch (err) {
        console.error("Failed to log in as an anonymous user.", err);
        return [];
    }
}

module.exports = { getRandomMovies, getMovieByTitle, getMovieByDirector };
