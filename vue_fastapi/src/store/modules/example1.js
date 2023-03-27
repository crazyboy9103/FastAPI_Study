const state = {
  example1: null,
};

const getters = {
  example1Getter(state) {
    return state.example1;
  }
};

const actions = {  

};

const mutations = {
  setExample1(state, text) {
    state.example1 = text;
  },
  reset1(state){
    state.example1 = null;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};