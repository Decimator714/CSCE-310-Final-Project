const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/mydatabase', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(() => {
  console.log('Connected to database');
}).catch((err) => {
  console.log('Error connecting to database:', err);
});

const dataSchema = new mongoose.Schema({
    // define your schema fields here
  });

const Data = mongoose.model('Data', dataSchema);

const app = express();

app.use(cors());
app.use(express.json());

app.get('/api/data', async (req, res) => {
  const data = await Data.find();
  res.send(data);
});

app.post('/api/data', async (req, res) => {
  const newData = new Data(req.body);
  await newData.save();
  res.send(newData);
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});
