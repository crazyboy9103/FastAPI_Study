<template>
    <div class="loginlog-comp">
        <p>{{ created_at}}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginLogComponent',
    props: {
      created_at: {
        type: String, 
        default: ''
      }
    },
  }
  </script>