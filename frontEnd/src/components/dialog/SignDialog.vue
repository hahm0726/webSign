<template>
  <v-card class="pa-2">
    <vue-signaturePad
      class="canvas-color"
      width="100%"
      height="200px"
      ref="signaturePad"
      :options="{
        onBegin: () => {
          $refs.signaturePad.resizeCanvas();
        },
      }"
    >
    </vue-signaturePad>
    <v-btn class="mt-2" small @click="clearCanvas">지우기</v-btn>
    <v-card-actions class="pa-0">
      <v-spacer></v-spacer>
      <v-btn color="error white--text" small @click="closeDialog">
        취소
      </v-btn>
      <v-btn color="blue darken-1 white--text" small @click="save">
        서명완료
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
      //canvas 비우기
      clearCanvas() {
        this.$refs.signaturePad.clearSignature();
      },
      //캔버스 내용 저장
      save() {
        const { isEmpty, data } = this.$refs.signaturePad.saveSignature();
        if(isEmpty){
          alert("서명해주세요.");
          return;
        }
        this.item.signature=data;
        this.item.state=true;
        
        const today = new Date();

        const year = today.getFullYear();
        let month = today.getMonth() +1;
        let date = today.getDate();

        month = ("0"+month).slice(-2);
        date = ("0"+date).slice(-2);

        this.item.receivedDate= year+"-"+month+"-"+date;
        
        billApi.updateBill(this.item.id,this.item)
        .then(()=>{
          this.closeDialog();
          this.$store.dispatch("callToast", {
            msg: "서명 완료",
            result: "success",
          });
          this.$emit('reRender');
        })
        .catch(()=>{
          this.$store.dispatch("callToast", {
            msg: "서명 실패",
            result: "fail",
          });
        });
      },

      //다이얼로그 닫기
      closeDialog() {
        this.$emit('closeDialog');
        this.clearCanvas();
      },
  }
}
</script>

<style scoped>
.canvas-color {
  background-color: lightgray;
  border: 1px solid black;
}
</style>