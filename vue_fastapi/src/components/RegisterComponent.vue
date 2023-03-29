<template>
  <div class="register-comp">
    <div>
      <input
        placeholder="이름"
        type="text"
        :value="name"
        @input="$emit('update:name', $event.target.value)"
      />
      <input
        placeholder="아이디"
        type="email"
        :value="email"
        @input="$emit('update:email', $event.target.value)"
      />
      <input
        placeholder="비밀번호"
        type="password"
        :value="password"
        @input="$emit('update:password', $event.target.value)"
      />
      <button @click="$emit('register')">
        회원가입
      </button>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'RegisterComponent',
  props: {
    name: {
      type: String,
      default: ''
    },
    email: {
      type: String,
      default: ''
    },
    password: {
      type: String,
      default: ''
    }
  },
  emits: ['register', 'update:name', 'update:email', 'update:password'],
  methods: {
    
  }
}
</script>