<template>
  <div class="example">
    <h1>This is an example page</h1>
    <p>{{ this.example1Getter }}</p>
    <div>
      <input v-model="text">
      <button @click="setExample1(text)">Change</button>
      <button @click="reset1(); text='';">Reset</button>
    </div>
  </div>
</template>

<script>

import axios from 'axios';
import { mapActions, mapMutations, mapGetters, mapState} from 'vuex'

export default {
  name: 'StoreExampleView',
  components: {
    
  },
  data() {
    return {
      text: '',
      api_url: '/api/example'
    }
  },

  mounted() {
    console.log("Example ")
    axios
      .get(this.api_url)
      .then((res) => {
        this.setExample1(this.api_url + " API 결과 :" + JSON.stringify(res.data))
      })
      .catch((err) => {
        this.setExample1(this.api_url + " API 결과 :" + JSON.stringify(err.message))
      })
  },

  computed: {
    // map states defined in store to this.example1, this.example2 
    ...mapState(['example1', 'example2']),
    // Can refer to 'name' state as this.newname
    // ...mapState({ 'newname': 'name' }) 
    // We do not access the state directly, better to use defined getters
    ...mapGetters(['example1Getter'])
  },

  methods: {
    ...mapMutations(['setExample1', 'setExample2', 'reset1', 'reset2']),
  }

}
</script>
