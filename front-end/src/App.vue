<template>
  <StartScreen></StartScreen>  
</template>

<script>
import StartScreen from './components/StartScreen.vue'

export default {
  name: 'App',
  components: {
    StartScreen
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-image: url('~@/assets/bg-image.svg');
  min-height: 100vh;
  min-width: 100vh;
  background-repeat: no-repeat;
  background-position-x: right;
}
html, body{
  background: black;
  border: 0;
  margin: 0;
}
</style>
