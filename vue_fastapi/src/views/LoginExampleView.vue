<template>
  <div class="login">
    <h1>This is an login page</h1>
    <div> 
      <div>
        <input :disabled="logined" v-model="username">
        <p>logined : {{ logined }}</p>
        <p>name : {{ myname }}</p>
      </div>
      <button @click="btnClick">{{ btnLabel }}</button>
    </div>
  </div>
</template>

<script>

import { mapActions, mapMutations, mapGetters, mapState} from 'vuex'

export default {
  name: 'LoginExampleView',
  components: {
    
  },
  data() {
    return {
      username: ''
    }
  },

  mounted() {
    console.log("Login")
  },

  computed: {
    ...mapGetters(['logined']),
    // map this.myname to store.state.username
    ...mapGetters({myname: 'username'}),
    btnLabel() {
      if (this.logined) {
        return "로그아웃";
      }
      return "로그인";
    }
  },

  methods: {
    ...mapMutations(['logOut']),
    ...mapActions(['login']),
    btnClick() {
      if (!this.logined) {
        this.login({name: this.username})
      } else {
        this.logOut()
      }
    }
  }

}
</script>
