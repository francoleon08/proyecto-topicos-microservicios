const Realm = require("realm-web");

const app = new Realm.App({ id: "application-mflix-yqrpksi" });

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

module.exports = { getRandomMovies };
