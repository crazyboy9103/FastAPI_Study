<template>
  <nav>
    <p>실행 모드: {{ APP_PHASE }}</p>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link> | 
    <router-link to="/example">Example</router-link> |
    <router-link to="/login">Login</router-link> |
    <router-link to="/user">User</router-link> |
    <router-link to="/auth/login">Auth Login</router-link>
  </nav>
  <router-view/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
<script>

export default {
  computed: {
    APP_PHASE() {
      return process.env.NODE_ENV;
    }
  },
}
</script>