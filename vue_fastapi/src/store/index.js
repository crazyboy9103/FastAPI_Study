import { createStore } from 'vuex';

import example1 from './modules/example1';
import example2 from './modules/example2';

import login from './modules/login';
import auth from './modules/auth';
export default createStore({
	modules: {
		example1,
		example2,
		login,
		auth
	},
});