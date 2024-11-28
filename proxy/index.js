const amqp = require("amqplib/callback_api");
const express = require("express");
const cors = require('cors');

const app = express();

const PORT = process.env.PORT || 3000;
const RABBIT_RECONNECT_TIMEOUT = process.env.RABBITMQ_RECONNECT_TIMEOUT || 5000;
const RABBIT_URL = process.env.RABBITMQ_URL;
const RABBIT_MOVIES_QUEUE = process.env.RABBITMQ_MOVIES_QUEUE;
const RABBIT_RECOMMENDATIONS_QUEUE = process.env.RABBITMQ_RECOMMENDATIONS_QUEUE;

let channel;
let movies = [];

app.use(cors());
app.use(express.json());

connectRabbitMQ()
  .then((connection) => {
    app.listen(PORT, () => {
      channel = connection.createChannel();
      consume_movies();
      console.log(`[*] Server is running on port ${PORT}`);
    });
  })
  .catch((error) => {
    console.error(`[!] Error connecting to RabbitMQ: ${error}`);
  });

app.post("/movie/viewed", (req, res) => {
  const movie = req.body;
  send_movie(movie);
  res.json({
    message: "Data received successfully!",
    data: movie,
  });
});

app.get("/movie/recommendation", async (req, res) => {
  const movie = movies.shift();
  res.json(movie);
});

function send_movie(movie) {
  const queue = RABBIT_MOVIES_QUEUE;
  const message = JSON.stringify(movie);
  channel.assertQueue(queue, { durable: true });
  channel.sendToQueue(queue, Buffer.from(message));
  console.log(`[x] Sent a message to ${queue}`);
}

function consume_movies() {
  const queue = RABBIT_RECOMMENDATIONS_QUEUE;
  channel.assertQueue(queue, { durable: true });
  channel.consume(
    queue,
    (message) => {
      if (message) {
        const content = message.content.toString();
        const movie = JSON.parse(content);
        movies.push(movie);
      }
    },
    { noAck: true },
  );
}

function connectRabbitMQ() {
  console.log(`[*] Trying to connect to RabbitMQ...`);
  return new Promise((resolve, reject) => {
    amqp.connect(RABBIT_URL, function (error, connection) {
      if (error) {
        setTimeout(
          () => connectRabbitMQ().then(resolve).catch(reject),
          RABBIT_RECONNECT_TIMEOUT,
        );
      } else {
        console.log(`[*] Connected to RabbitMQ`);
        resolve(connection);
      }
    });
  });
}
