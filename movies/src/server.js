const express = require('express');
const movieRoutes = require('./routes/routes');

const app = express();
const port = 3000;

app.use(express.json());

app.use('/api', movieRoutes);

app.listen(port, () => {
  console.log(`Server listening to http://localhost:${port}`);
});