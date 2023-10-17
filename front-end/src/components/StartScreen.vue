<template>
  <div class="startScreenContainer">
    <div class="headerSection">
      <div class="headerText">Image Alchemy</div>
      <div class="headerTextDescription">
        The digital canvas where your imagination meets modern art. With a few
        clicks, you can turn your ordinary images into extraordinary pieces of
        contemporary art.
      </div>
      <button class="uploadImageButton" @click="onUploadClick">
        Upload image
      </button>
      <input
        type="file"
        accept="image/png, image/jpeg"
        @input="onFileUpload"
        single
        ref="fileInput"
        hidden
      />
    </div>
    <div class="imagesContainer" v-if="imagesData[0]">
      <ImageItem
        class="firstImage"
        :imageSrc="imagesData[0]?imagesData[0].dataSource:null"
        imageTitle="Input image"
        @click="show(0)"
      ></ImageItem>
      <div class="generatedImagesContainer">
        <ImageItem
          imageTitle="Cubism"
          :imageSrc="imagesData[1] ? imagesData[1].dataSource: null"
          @click="show(1)"
        ></ImageItem>
        <ImageItem
          imageTitle="Pointillism"
          :imageSrc="imagesData[2] ? imagesData[2].dataSource: null"
          @click="show(2)"
        ></ImageItem>
        <ImageItem
          imageTitle="New Realism"
          :imageSrc="imagesData[3]?imagesData[3].dataSource:null"
          @click="show(3)"
        ></ImageItem>
      </div>
    </div>
  </div>
</template>

<script>
import ImageItem from "./ImageItem.vue";
import "viewerjs/dist/viewer.css";
import { api as viewerApi } from "v-viewer"

export default {
  components: {
    ImageItem,
  },
  data() {
    return {
      imagesData: [null, null, null, null],
      viewerActive: false,
      options: {
        toolbar: true,
        url: "dataSource",
        initialViewIndex: 1,
      },
    };
  },
  computed: {
    computedImages() {
      return this.imagesData.filter((x) => x != null);
    },
  },
  methods: {
    onUploadClick() {
      this.$refs.fileInput.click();
    },
    onFileUpload(e) {
      if (e.target.files.length > 0) {
        let fr = new FileReader();
        fr.onload = () => {
          this.imagesData[0] = {dataSource:fr.result};
          this.uploadImageandGetGeneratedImages();
        };
        fr.readAsDataURL(e.target.files[0]);
      }
    },
    uploadImageandGetGeneratedImages() {
      const url = "http://localhost:8000/upload";

      const requestData = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          image: this.imagesData[0],
        }),
      };

      fetch(url, requestData)
        .then((response) => response.json())
        .then((data) => {
          for(var i=1;i<data.length+1;i++){
            this.imagesData[i] = data[i-1]
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
    inited(viewer) {
      this.$viewer = viewer;
    },
    show(index) {
      //this.options.initialViewIndex = index+1;
        const $viewer = viewerApi({
          options: {
            toolbar: true,
            url: 'dataSource',
            initialViewIndex: index
          },
          images: this.computedImages
        })
        $viewer.show()
    },
  },
};
</script>

<style lang="scss" scoped>
.headerText {
  font-family: Georgia, serif;
  font-size: 4em;
  color: white;
  text-align: left;
}
.headerTextDescription {
  font-family: "Roboto";
  color: white;
  text-align: left;
  font-size: 20px;
  margin-top: 18px;
  width: 40%;
}

.startScreenContainer {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.headerSection {
  min-height: 35vh;
  margin-top: 10vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.uploadImageButton {
  color: black;
  border-radius: 5px;
  background: #b8afda;
  margin: 30px 0px;
  padding: 14px 28px;
  border: none;
  width: fit-content;
  font-size: 18px;
  cursor: pointer;
  font-weight: 600;
  &:hover {
    background: adjust-color($color: #b8afda, $lightness: -5%);
  }
  &:active {
    background: adjust-color($color: #b8afda, $lightness: -10%);
  }
}

.imagesContainer {
  display: flex;
  flex-flow: wrap;
}
.generatedImagesContainer {
  background: #383838;
  border-radius: 10px;
  display: flex;
  flex-flow: wrap;
  padding-left: 20px;
  padding-right: 20px;
  margin-left: 20px;
}

.firstImage {
  border-left: 0px;
}
</style>