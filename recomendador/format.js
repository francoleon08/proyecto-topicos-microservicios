const fs = require('fs');
const axios = require('axios');
const amqp = require('amqplib/callback_api');
const { exec } = require('child_process');
const json2csv = require('json2csv').parse; 

const RABBITMQ_URL = 'amqp://rabbitmq:5672';
const QUEUE_NAME = 'movies';
const RESULT_QUEUE = 'recommendations';

const MOVIES_SERVICE_URL = 'http://movies:3000/movies';
const MOVIE_HISTORY_FILE = './database/movies.csv'; 
const RECOMMENDABLE_MOVIES_FILE = './database/recommendable.csv'; 

amqp.connect(RABBITMQ_URL, (err, connection) => {
    if (err) {
        console.error('Failed to connect to RabbitMQ:', err);
        return;
    }
    console.log('Connected to RabbitMQ');

    connection.createChannel((err, channel) => {
        if (err) {
            console.error('Failed to create a channel:', err);
            return;
        }
        console.log('Channel created');

        channel.assertQueue(QUEUE_NAME, { durable: true });
        channel.assertQueue(RESULT_QUEUE, { durable: true });

        console.log(`Waiting for messages in queue: ${QUEUE_NAME}`);

        channel.consume(
            QUEUE_NAME,
            async (msg) => {
                if (msg !== null) {
                    const movieHistory = JSON.parse(msg.content.toString());
                    console.log('Received movie history:', movieHistory);

                    try {
                        storeMovieHistory(movieHistory);
                    } catch (err) {
                        console.error('Error storing movie history:', err);
                    }

                    try {
                        const recommendableMovies = await fetchRecommendableMovies();

                        storeRecommendableMovies(recommendableMovies);

                        const recommendations = await runPythonScript({
                            history: movieHistory,
                            recommendableMovies,
                        });

                        console.log('Recommendations:', recommendations);

                        const resultMessage = JSON.stringify({
                            history: movieHistory,
                            recommendations,
                        });
                        channel.sendToQueue(RESULT_QUEUE, Buffer.from(resultMessage));
                        console.log('Sent recommendations to RESULT_QUEUE:', resultMessage);

                        channel.ack(msg);
                    } catch (err) {
                        console.error('Error processing message:', err);
                        channel.nack(msg, false, false); 
                    }
                }
            },
            { noAck: false }
        );
    });
});

async function fetchRecommendableMovies() {
    try {
        const response = await axios.get(MOVIES_SERVICE_URL);
        console.log('Fetched recommendable movies:', response.data);
        return response.data; 
    } catch (err) {
        console.error('Error fetching recommendable movies:', err);
        throw err;
    }
}

function runPythonScript(data) {
    return new Promise((resolve, reject) => {
        const child = exec('python recommendation.py', (err, stdout, stderr) => {
            if (err) {
                return reject(stderr || err.message);
            }
            resolve(JSON.parse(stdout.trim())); 
        });
        child.stdin.write(JSON.stringify(data)); 
        child.stdin.end();
    });
}

function storeMovieHistory(movieHistory) {
    const csvData = movieHistory.map(movie => ({
        title: movie.title,
        genre: movie.genre,
        timestamp: movie.timestamp, 
    }));

    const csv = json2csv(csvData);

    fs.appendFileSync(MOVIE_HISTORY_FILE, csv + '\n', 'utf8');
    console.log('Stored movie history in CSV file');
}

function storeRecommendableMovies(recommendableMovies) {
    const csvData = recommendableMovies.map(movie => ({
        id: movie.id,                         
        title: movie.title,                   
        genre: movie.genre,                   
        plot: movie.plot,                     
        poster: movie.poster,                 
        description: movie.description,       
        release_date: movie.released     
    }));

    const csv = json2csv(csvData);

    fs.appendFileSync(RECOMMENDABLE_MOVIES_FILE, csv + '\n', 'utf8');
    console.log('Stored recommendable movies in CSV file');
}