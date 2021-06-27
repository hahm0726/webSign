<template>
  <v-app id="app">
    <v-dialog
      v-model="excelDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <excel-board @closeExcelDialog="closeExcelDialog"></excel-board>
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
        <v-btn id="add-data-btn" elevation="0">
          <span class="btn-text">데이터 추가</span>
          <v-icon class="icon-in-btn">mdi-plus</v-icon>
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

export default {
  components: {
    Board,
    ExcelBoard,
  },
  data: () => ({
    excelDialog: false,
  }),
  computed: {
    //선택된 컴포넌트 반환
    selectedComponent: function () {
      return Board;
    },
  },
  methods: {
    //다이얼로그 열기
    openExcelDialog() {
      this.excelDialog = true;
    },
    //다이얼로그 닫기
    closeExcelDialog() {
      this.excelDialog = false;
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