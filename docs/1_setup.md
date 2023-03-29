# FastAPI-Vue 통신 (Vue 가이드 페이지 템플릿)
> - 경로를 표시할때 백엔드 폴더경로 ```backend/```와 프론트엔드 경로```vue_fastapi/src/```는 생략
> - ```.vue``` 파일이면 프론트엔드, ```.py``` 면 백엔드
## 목차 
- [FastAPI-Vue 통신 (Vue 가이드 페이지 템플릿)](#fastapi-vue-통신-vue-가이드-페이지-템플릿)
  - [목차](#목차)
  - [프록시 설정](#프록시-설정)
  - [실행 모드](#실행-모드)
  - [예제](#예제)
    - [필요한 View 작성](#필요한-view-작성)
    - [필요한 Store 작성](#필요한-store-작성)
    - [해당 View를 보여주기 위해 수정](#해당-view를-보여주기-위해-수정)
    - [필요한 백엔드 작성](#필요한-백엔드-작성)
    - [라우트 연결](#라우트-연결)
    - [접속 방법](#접속-방법)

---
## 프록시 설정
> FastAPI에서는 8000포트를 사용하고 Vue에서는 8080포트를 사용하기 위해서 프록시를 설정 
> ```vue.conig.js```
```
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,

    devServer: {
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    },
        
    outputDir: '../backend/public'
})
```

## 실행 모드 
> 프로덕션, 개발 모드를 설정하기 위해서 ```"scripts"```에 ```"prod", "dev"``` 추가
> ```package.json```
```
"scripts": {
    "prod": "vue-cli-service serve --mode prod",
    "dev": "vue-cli-service serve --mode dev"
},
```
---
## 예제
### 필요한 View 작성 
> ```views/LoginExampleView.vue```
* ```username```을 입력하고 버튼을 누르면 서버에 요청을 보냄
* 결과를 받은 경우 ```<input>```을 disable시킴
* 다시 버튼을 누르면 저장된 정보를 없애고 다시 enable
```
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
```

* 해당 View에서 함수를 정의하지 않고, ```store/modules/login.js```에 관련 변수, 함수 등을 정의해 놓고, ```...mapMutations, ...mapActions, ...mapGetters, ...mapState```를 사용해서 처리
```
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
```

### 필요한 Store 작성     
> ```store/modules/login.js```
필요한 변수인 ```user```는 ```state```에 작성
```
const state = {
    user: null
};
```

해당 ```state```를 사용해서 ```store```에 저장된 값을 받아오는 ```getters```에 함수를 작성 
```
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
```

비동기로 작동하는 경우 ```actions```에 함수를 작성
```
import axios from 'axios';
const actions = {  
    login({commit, state}, payload) {
        return axios.post("/api/login", payload)
            .then((res) => {
                commit("setUser", res.data); # setUser라는 mutation을 commit
                                                # commit이란 mutation을 동기적으로 실행시키는 것
                                                # 비동기 작업이 모두 끝난후 성공적이면 setUser를 실행
            })
            .catch((err) => {
                commit("logOut");            # 에러가 발생하면 logOut을 실행 
            })
    }
};
```

```state```의 변수를 변경하려면 외부에서 직접 변경하지 말고 ```mutations```에 함수를 작성
```
const mutations = {
    setUser: function(state, payload) {
        state.user = payload;
    },

    logOut: function(state) {
        state.user = null;
    }
};
```

마지막으로 이 4개를 묶어서 ```export default```
```
export default {
    state,
    getters,
    actions,
    mutations
};
```

```store/index.js```에 이렇게 작성하면 이 파일에서 정의한 ```state, getters, actions, mutations```을 불러올 수 있게 해줌
```
import { createStore } from 'vuex';
import login from './modules/login';
import createPersistedState from 'vuex-persistedstate'; 
export default createStore({
    modules: {
        login,
    },
    plugins: [createPersistedState()]
});
```

### 해당 View를 보여주기 위해 수정
> ```router/index.js, App.vue```
아래 코드를 ```router/index.js```에 작성하면 ```/login```으로 라우트될때 ```LoginExampleView.vue```를 렌더링함
```
const routes = [
    ...
    {
        path: '/login',
        name: 'login',
        component: () => import('../views/LoginExampleView.vue')
    },
    ...
]
```

```App.vue```에 해당 URL로 가는 ```router-link```를 작성
```
<router-link to="/login">Login</router-link> 
```

### 필요한 백엔드 작성
> ```routes/login.py```   
```username```을 받고 해당 객체를 다시 돌려주는 간단한 백엔드
``` 
from fastapi import APIRouter
from pydantic import BaseModel # 모델을 작성하는데 필요한 도구 
                                # 간단한 폼같은거 작성할때 BaseModel을 상속해서 작성해놓으면 FastAPI docs에서 볼수있음

class User(BaseModel): # User를 생성하고, str 타입인 name을 지정
    name: str

router = APIRouter() # 라우터를 생성

@router.post( # /login 에 post 요청시 불리는 함수 login 정의
    "/login"
)
async def login(user: User): # User 형태를 가지는 요청을 받고, 돌려주는 함수 
    return user
```

### 라우트 연결
> ```main.py```
> 위에서 작성한 라우트는 ```main.py```에서 실행되는 FastAPI 앱에서는 아직 접근이 불가능함 

```routes/login.py```에서 생성한 router를 ```app```에 추가시켜야 함 
```
from routes import login
app.include_router(login.router)
```

### 접속 방법 
```backend``` 폴더에서 백엔드 서버를 실행 
```
# backend/README.md 참고
poetry shell
uvicorn main:app --reload
```

```vue_fastapi``` 폴더에서 프론트엔드를 실행 
```
# vue_fastapi/README.md 참고
npm run dev
```

```127.0.0.1:8080``` 에 접속하면 메인 화면이 뜨고, 상단에 Login을 클릭