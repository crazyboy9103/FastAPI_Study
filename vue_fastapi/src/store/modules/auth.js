import axios from 'axios';
const state = {
  access_token: null,
  refresh_token: null
};
  
const getters = {
  accessToken(state){
    return state.access_token;
  },
  refreshToken(state){
    return state.refresh_token;
  },
  axiosconfig(state){
    if (!state.access_token) return {}
    return {headers: {Authorization: `Bearer ${state.access_token}`}}
  }
};

const actions = {  
  // Register
  register({commit, state}, payload) {
    return axios.post('/api/auth/users', payload)
    .then((res) => {
      console.log("register success")
      console.log(res.data);
    })
    .catch((err) => {
      console.log("register fail")
      console.log(err.data);
    })
  },
  // Get new access token (same as login)
  getToken({commit, state}, payload) {
    var form_data = new FormData();
    for ( var key in payload ) {
      form_data.append(key, payload[key]);
    }
    return axios.post('/api/auth/login', form_data)
    .then((res) => {
      console.log("getToken success")
      console.log(res)
      commit("setAccessToken", res.data);
    })
    .catch((err) => {
      console.log("getToken fail")
      console.log(err)
    })
  },
  // Use refresh token to get new access token
  getNewToken({commit, state, getters}) {
    return axios.post('/api/auth/new_token', {refresh_token: getters.refresh_token})
    .then((res) => {
      console.log("getNewToken success")
      console.log(res)
      commit("setAccessToken", res.data);
    })
    .catch((err) => {
      console.log("getNewToken fail")
      console.log(err)
    })
  },

  // Use access token to get my info
  getMe({commit, state, getters}, payload) {
    return axios.get('/api/auth/me', getters.axiosconfig)
    .then((res) => {
      console.log("getme success")
      console.log(res);
      payload.name = res.data.name;
      payload.email = res.data.email;
      payload.password = res.data.password;
    })
    .catch((err) => {
      console.log("getme fail")
      console.log(err.data);
    })
  },

  // Use access token to get my login logs
  getMyLoginLogs({commit, state, getters}, payload) {
    payload.length = 0;
    return axios.get('/api/auth/me/loginLogs', getters.axiosconfig)
    .then((res) => {
      console.log("loginLogs success")
      console.log(res);
      payload.push(...res.data);
    })
    .catch((err) => {
      console.log("loginLogs fail")
      console.log(err.data);
    })
  },
  
};

const mutations = {
  setAccessToken: function(state, payload) {
    state.access_token = payload.access_token;
    state.refresh_token = payload.refresh_token;    
  },

  resetAccessToken: function(state) {
    state.access_token = null;
    state.refresh_token = null;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};