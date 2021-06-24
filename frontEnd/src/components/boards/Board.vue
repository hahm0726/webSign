<template>
  <v-data-table class="tables" :headers="thItems" :items="tdItems">
    <template v-slot:top>
      <v-dialog v-model="dialog" persistent max-width="500px">
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
            <v-btn color="blue darken-1 white--text" small @click="closeDialog">
              서명완료
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </template>

    <template v-slot:[`item.receivedDate`]="{ item }">
      {{ receivedDate(item.receivedDate) }}
    </template>
    <template v-slot:[`item.state`]="{ item }">
      {{ isReceived(item.state) }}
    </template>
    <template v-slot:[`item.action`]="{ item }">
      <v-btn v-if="item.state" @click="openDialog(item)">서명확인</v-btn>
      <v-icon v-else :disabled="item.state" @click="openDialog(item)">
        fa-file-signature
      </v-icon>
    </template>
  </v-data-table>
</template>

<script>
export default {
  data: () => ({
    dialog: false,
    thItems: [
      { text: "연번", value: "idx", align: "center" },
      { text: "이름", value: "name", align: "center" },
      { text: "거주동", value: "location", align: "center" },
      { text: "수량", value: "amount", align: "center" },
      { text: "수령일", value: "receivedDate", align: "center" },
      { text: "수령상태", value: "state", align: "center" },
      { text: "작업", value: "action", align: "center" },
    ],
    tdItems: [
      {
        idx: 1,
        name: "홍길동",
        location: "안양2동",
        amount: 1,
        receivedDate: null,
        state: true,
      },
      {
        idx: 1,
        name: "홍길동",
        location: "안양2동",
        amount: 1,
        receivedDate: null,
        state: true,
      },
      {
        idx: 1,
        name: "홍길동",
        location: "안양2동",
        amount: 1,
        receivedDate: null,
        state: true,
      },
      {
        idx: 1,
        name: "홍길동",
        location: "안양2동",
        amount: 1,
        receivedDate: null,
        state: true,
      },
      {
        idx: 1,
        name: "홍길동",
        location: "안양2동",
        amount: 1,
        receivedDate: null,
        state: true,
      },
      {
        idx: 2,
        name: "김상만",
        location: "안양1동",
        amount: 2,
        receivedDate: null,
        state: false,
      },
      {
        idx: 3,
        name: "최길자",
        location: "안양1동",
        amount: 1,
        receivedDate: null,
        state: false,
      },
    ],
  }),

  methods: {
    // 수령 상태 출력 변환
    isReceived: function (val) {
      if (val === true) return "수령완료";
      return "수령 전";
    },
    //수령날짜 출력 변환
    receivedDate: function (val) {
      if (val === null) return "수령 전";
      return val;
    },
    //다이얼로그 열기
    openDialog() {
      this.dialog = true;
    },
    //다이얼로그 닫기
    closeDialog() {
      this.dialog = false;
      this.clearCanvas();
    },

    clearCanvas() {
      this.$refs.signaturePad.clearSignature();
    },
    save() {
      const { isEmpty, data } = this.$refs.signaturePad.saveSignature();
      console.log(isEmpty);
      console.log(data);
    },
  },
};
</script>

<style scoped>
.tables {
  width: 100%;
  max-width: 1200px;
}
.canvas-color {
  background-color: lightgray;
  border: 1px solid black;
}
</style>