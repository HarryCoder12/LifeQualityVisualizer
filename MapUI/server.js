const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.static(__dirname));

app.listen(8000, () => console.log('Server running on http://localhost:8000'));
