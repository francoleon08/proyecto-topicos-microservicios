const express = require('express');
const movieRoutes = require('./routes/routes');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.use('/movies', movieRoutes);

app.listen(port, () => {
  console.log(`Server listening to http://localhost:${port}`);
});