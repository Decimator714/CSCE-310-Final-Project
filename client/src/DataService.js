import axios from 'axios';

const DataService = {
  async getAll() {
    const response = await axios.get('/data');
    return response.data;
  },

  async create(data) {
    const response = await axios.post('/data', data);
    return response.data;
  }
}

export default DataService;
