import axios from 'axios';
const state = {
  user: null
};
  
const getters = {
  logined(state) {
    return state.user !== null;
  },

  username(state) {
    if (state.user) {
      return state.user.name;
    } else {
      return '';
    }
  }
};

const actions = {  
  login({commit, state}, payload) {
    return axios.post("/api/login", payload)
    .then((res) => {
      commit("setUser", res.data);
    })
    .catch((err) => {
      commit("logOut");
    })
  }
};

const mutations = {
  setUser: function(state, payload) {
    state.user = payload;
  },

  logOut: function(state) {
    state.user = null;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};