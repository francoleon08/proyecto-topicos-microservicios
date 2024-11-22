const express = require('express');
const cors = require('cors');
const movieRoutes = require('./routes/routes');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());

app.use(express.json());

app.use('/movies', movieRoutes);

app.listen(port, () => {
  console.log(`Server listening to http://localhost:${port}`);
});