<template>
  <v-app id="app">
    <v-dialog
      v-model="dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
      persistent
    >
      <component :is="selectedBoard" @closeDialog="closeDialog"></component>
    </v-dialog>
    <header id="app-header">
      <v-spacer />
      <div class="btn-group">
        <v-btn id="load-excel-btn" elevation="0" @click="openExcelDialog">
          <span class="btn-text">Excel 불러오기</span>
          <v-icon class="icon-in-btn" color="rgb(31, 111, 68)">
            mdi-microsoft-excel
          </v-icon>
        </v-btn>
        <v-btn id="add-data-btn" elevation="0" @click="openUpdateDialog">
          <span class="btn-text">데이터 수정</span>
          <v-icon class="icon-in-btn">mdi-pencil-outline</v-icon>
        </v-btn>
      </div>
    </header>
    <v-main>
      
      <v-container id="contents-wrap" class="pt-2">
        <component :is="selectedComponent"></component>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Board from "/src/components/boards/Board";
import ExcelBoard from "/src/components/boards/ExcelBoard";
import UpdateBoard from "/src/components/boards/UpdateBoard";

export default {
  components: {
    Board,
    ExcelBoard,
    UpdateBoard,

  },
  data: () => ({
    dialog:false,
    excelDialog: false,
    updateDialog: false,
    selectedBoard:null,
  }),
  computed: {
    //선택된 컴포넌트 반환
    selectedComponent: function () {
      return Board;
    },
    
  },
  methods: {
    //엑셀 다이얼로그 열기
    openExcelDialog() {
      this.selectedBoard=ExcelBoard,
      this.excelDialog = true;
      this.dialog = this.excelDialog;
    },
    //엑셀 다이얼로그 닫기
    closeExcelDialog() {
      this.excelDialog = false;
      this.dialog = this.excelDialog;
    },
    //수정 다이얼로그 열기
    openUpdateDialog() {
      this.selectedBoard=UpdateBoard,
      this.updateDialog = true;
      this.dialog = this.updateDialog;
    },
    //수정 다이얼로그 닫기
    closeUpdateDialog() {
      this.updateDialog = false;
      this.dialog = this.updateDialog;
    },
    //열린 다이얼로그에 따라 다이얼로그 닫기 함수 선택 제공
    closeDialog() {
      if(this.excelDialog) return this.closeExcelDialog();
      if(this.updateDialog) return this.closeUpdateDialog();
    },
  },
};
</script>

<style scoped>
#app {
  padding: 0;
  width: 100%;
}
#app-header {
  display: flex;
  align-items: center;
  width: 100%;
  height: 60px;
  border: 2px solid;
}
.btn-group {
  display: flex;
  justify-items: end;
  margin-right: 8px;
  margin-left: 8px;
}
.icon-in-btn {
  margin-left: 4px;
}
#load-excel-btn {
  background-color: white;
  border: 1px solid;
  text-align: center;
  margin-right: 8px;
}
#add-data-btn {
  background-color: white;
  border: 1px solid;
  text-align: center;
}
#contents-wrap {
  min-height: 90vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.btn-text {
  display: initial;
}

@media screen and (max-width: 600px) {
  .btn-text {
    display: none;
  }
}
</style>