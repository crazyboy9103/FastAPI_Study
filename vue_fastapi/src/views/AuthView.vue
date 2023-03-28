<template>
    <div class="auth">
      <h1>This is auth example page</h1>
      
      <AuthComponent
        @login="getTokenAndMyInfo(login_form)"
        v-model:email="login_form.username"
        v-model:password="login_form.password" />
      
      <RegisterComponent
        @register="register(register_form)"
        v-model:name="register_form.name"
        v-model:email="register_form.email"
        v-model:password="register_form.password" />

      <div v-if="login_logs">
        <LoginLogComponent
          v-for="(log, idx) in login_logs"
          :key=idx
          :created_at="log.created_at"
          />
      </div>
    </div>
  </template>
  
  <script>
  
  import axios from 'axios'
  import { mapActions, mapMutations, mapGetters, mapState} from 'vuex'
  
  import AuthComponent from '@/components/AuthComponent.vue'
  import RegisterComponent from '@/components/RegisterComponent.vue'
  import LoginLogComponent from '@/components/LoginLogComponent.vue'
  export default {
    name: 'AuthView',
    components: {
        AuthComponent, RegisterComponent, LoginLogComponent
    },
  
    data() {
      return {
        login_form: {
          username: '', 
          password: ''
        },
        register_form: {
          name: '',
          email: '', 
          password: ''
        },
        login_logs: [],
        me: {
          name: '', 
          email: '',
          password: ''
        }
      }
    },
  
    mounted() {
      console.log("Access Token: " + this.accessToken)
      console.log("Refresh Token: " + this.refreshToken)
      console.log("Header: " + this.axiosconfig)
    },
  
    computed: {
      ...mapGetters(['accessToken', 'refreshToken', 'axiosconfig'])
    },
  
    methods: {
      ...mapMutations(['setAccessToken', 'resetAccessToken']),
      ...mapActions(['register', 'getToken', 'getNewToken', 'getMe', 'getMyLoginLogs']),

      async getTokenAndMyInfo(form) {
        await this.getToken(form)
        await this.getMe(this.me)
        await this.getMyLoginLogs(this.login_logs)
        console.log(this.me)
        console.log(this.login_logs)
      }
    }
  
  }
  </script>
  