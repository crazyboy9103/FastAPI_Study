<template>
  <div class="auth-comp">
    <div>
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
      <button @click="$emit('login')">
        로그인
      </button>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'AuthComponent',
  props: {
    email: {
      type: String,
      default: ''
    },
    password: {
      type: String,
      default: ''
    }
  },
  emits: ['login', 'update:email', 'update:password'],
  methods: {
    
  }
}
</script>