const state = {
  example2: null,
};
  
const getters = {
  
};

const actions = {  

};

const mutations = {
  setExample2(state, text) {
    state.example2 = text;
  },
  reset2(state){
    state.example2 = null;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};