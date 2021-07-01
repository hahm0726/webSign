<template>
  <v-card class="pa-2">
    <img class="signature-img canvas-color" :src="item.signature">
    <v-card-actions class="pa-0">
      <v-spacer></v-spacer>
      <v-btn small @click="closeDialog">
        닫기
      </v-btn>
      <v-btn color="error" small @click="deleteSignautre">
        서명삭제
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import * as billApi from "/src/api/billApi"

export default {
  props:{
    item:Object,
  },
  methods:{
      //다이얼로그 닫기
      closeDialog() {
        this.$emit('closeDialog');
      },
      deleteSignautre(){
        if(confirm("서명을 삭제하시겠습니까?")){
          this.item.signature=null;
          this.item.state=false;
          this.item.receivedDate= null;
  
          billApi.updateBill(this.item.idx,this.item)
          .then(()=>{
            this.closeDialog();
          })
          .catch(err=>{console.log(err)});
        }else{
          return;
        }
      },
  }
}
</script>

<style scoped>
.canvas-color {
  background-color: lightgray;
  border: 1px solid black;
}

.signature-img{
  width:100%;
  height:200px;
}
</style>