import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:3000/api';

createApp(App).mount('#app')
