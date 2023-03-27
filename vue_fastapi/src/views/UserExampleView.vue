<template>
  <div class="user">
    <h1>This is an user page</h1>
    <div> 
      <div>
        <input placeholder="유저 고유번호" v-model="user_id">
        <div>
          <button @click="getUser()">유저 가져오기</button>
          <button @click="deleteUser()">유저 삭제하기</button>
        </div>
        <table style="margin-left: auto;margin-right: auto;">
          <th>이름</th>
          <th>이메일</th>
          <tr> 
              <td> {{ user.name }} </td>
              <td> {{ user.email }} </td>
          </tr>
        </table>
      </div>

      <div>
        <input placeholder="새 유저 이름" v-model="new_user.name">
        <input placeholder="새 유저 이메일" v-model="new_user.email">
        <input placeholder="새 유저 비밀번호" v-model="new_user.password">
        <button @click="createUser();">새 유저 생성</button>
      </div>

      <button @click="getUsers()">유저 리스트 가져오기</button>
      <table style="margin-left: auto;margin-right: auto;">
        <th>순서</th>
        <th>이름</th>
        <th>이메일</th>
        <tr v-for="(u, idx) of users" :key="idx"> 
            <td> {{ idx }} </td>
            <td> {{ u.name }} </td>
            <td> {{ u.email }} </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import { mapActions, mapMutations, mapGetters, mapState} from 'vuex'

export default {
  name: 'UserExampleView',
  components: {
    
  },
  data() {
    return {
      user_id: '',
      user: {
        name: '',
        email: '',
        password: ''
      },
      new_user: {
        name: '',
        email: '',
        password: ''
      },
      users: []
    }
  },

  mounted() {
    console.log("User")
    this.getUsers()
  },

  computed: {
  
  },

  methods: {
    resetUser() {
      this.user = {
        name: '',
        email: '',
        password: ''
      }
    },
    deleteUser() {
      if (!this.user_id) {
        alert("유저 고유번호를 입력해야합니다")
        return;
      }
      axios
      .delete('/api/user/'+this.user_id)
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      })

      this.getUsers();
    },
    getUser() {
      if (!this.user_id) {
        alert("유저 고유번호를 입력해야합니다")
        return;
      }
      axios
      .get('/api/user/'+this.user_id)
      .then((res) => {
        console.log(res);
        this.user = res.data;
      })
      .catch((err) => {
        console.log(err);
        this.resetUser()
      })
    },
    getUsers() {
      axios
      .get('/api/users')
      .then((res) => {
        console.log(res);
        this.users = res.data;
      })
      .catch((err) => {
        console.log(err);
      })
    },
    createUser() {
      if (!(this.new_user.name && this.new_user.email && this.new_user.password)) {
        alert("모든 필드를 입력해야합니다")
        return;
      }
      axios
      .post('/api/users', this.new_user)
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      })
      this.getUsers();
    }
  }

}
</script>
