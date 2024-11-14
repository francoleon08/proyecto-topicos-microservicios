const redis = require('redis');

const REDIS_URL = process.env.REDIS_URL;
const redisClient = redis.createClient({ url: REDIS_URL });
const CACHE_EXPIRATION_TIME = 60;

redisClient.on('error', (err) => {
    console.error('Redis Client Error', err);
});

redisClient.connect()
    .then(() => {
        redisClient.flushAll();    
        console.log('Redis client connected and flushed');
    })
    .catch((err) => {
        console.error('Redis client connection error', err);
    });


async function getFromCache(key) {
    if (await redisClient.exists(key)) {
        return JSON.parse(await redisClient.get(key));
    }
    return null;
}

async function cacheResult(key, value) {
    await redisClient.set(key, JSON.stringify(value), 'EX', CACHE_EXPIRATION_TIME);
}

module.exports = {getFromCache, cacheResult};
