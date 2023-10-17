<template>
  <div class="imgContainer">
    <div class="actualImageContianer">
        <img v-if="props.imageSrc" :src="props.imageSrc" class="currentImage"/>
        <div v-else class="imgLoadingScreen"></div>
    </div>
    <div class="imageText">{{props.imageTitle}}</div>
  </div>
</template>

<script setup>
    import { defineProps } from 'vue'

    const props = defineProps({
        imageTitle: String,
        imageSrc: String,
    })
</script>

<style lang="scss" scoped>
@keyframes placeholderShimmer {
  0% {
    background-position: -468px 0;
  }
  
  100% {
    background-position: 468px 0; 
  }
}
.imgLoadingScreen {
  border-radius: 5px;
  background: #FFFFFF;
  background-image: linear-gradient(to right, #ffffff 0%, #d2d3d4 40%, #c7c8c9 60%, #ffffff 100%);
  background-repeat: no-repeat;
  background-size: 468px 1004px; 
  display: inline-block;
  position: relative; 
  
  animation-duration: 2s;
  animation-fill-mode: forwards; 
  animation-iteration-count: infinite;
  animation-name: placeholderShimmer;
  animation-timing-function: linear;
  animation-timing-function: cubic-bezier(.44, .75, .2, 1.01);

  width: 100%;
  height: 100%;
  position: absolute;
  left: 0;
 }


.currentImage{
    max-width: 100%;
    max-height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.actualImageContianer{
    flex: 1;
    overflow: hidden;
    position: relative;
    background: #FFF;
    border-radius: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.imgContainer{
    min-width: 70px;
    min-height: 120px;
    overflow: hidden;
    width:200px;
    height:320px;
    max-width:200px;
    border-left: 20px solid transparent;
    border-right: 20px solid transparent;
    border-top: 40px solid transparent;
    border-bottom: 26px solid transparent;
    display: flex;
    flex-direction: column;
}

.imageText{
    padding-top: 10px;
    color: white;
    font-family: 'Roboto', sans-serif;
}


</style>