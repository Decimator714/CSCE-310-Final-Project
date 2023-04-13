<template>
  <div class="home">
    <h1>Data List</h1>
    <ul>
      <li v-for="data in dataList" :key="data._id">{{ data.title }}</li>
    </ul>
    <form @submit.prevent="addData">
      <input type="text" v-model="title">
      <button type="submit">Add</button>
    </form>
  </div>
</template>

<script>
import DataService from '../DataService';

export default {
  data() {
    return {
      dataList: [],
      title: ''
    };
  },
  async created() {
    this.dataList = await DataService.getAll();
  },
  methods: {
    async addData() {
      const data = { title: this.title };
      const newData = await DataService.create(data);
      this.dataList.push(newData);
      this.title = '';
    }
  }
}
</script>
