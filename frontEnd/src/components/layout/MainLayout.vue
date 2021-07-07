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
      <div class="logo-area">
        <v-img id="logo" :src="require(`/src/assets/logo.png`)"></v-img>
      </div>
      <v-spacer />
      <div class="btn-group">
        <v-btn id="add-user-btn" v-if="renderByUserType" elevation="0" @click="openUserDialog">
          <span class="btn-text">사용자 관리</span>
          <v-icon class="icon-in-btn">
            mdi-account-multiple
          </v-icon>
        </v-btn>
        <v-btn id="load-excel-btn" v-if="renderByUserType" elevation="0" @click="openExcelDialog">
          <span class="btn-text">Excel 불러오기</span>
          <v-icon class="icon-in-btn" color="rgb(31, 111, 68)">
            mdi-microsoft-excel
          </v-icon>
        </v-btn>
        <v-btn id="add-data-btn" v-if="renderByUserType" elevation="0" @click="openUpdateDialog">
          <span class="btn-text">데이터 수정</span>
          <v-icon class="icon-in-btn">mdi-pencil-outline</v-icon>
        </v-btn>
        <v-btn id="logout-btn" elevation="0" @click="logout">
          <span class="btn-text">로그아웃</span>
          <v-icon class="icon-in-btn">mdi-logout-variant</v-icon>
        </v-btn>
      </div>
    </header>
    <v-main class="main">
      <!-- 토스트 메시지 -->
      <v-snackbar
        id="snackbar"
        :color="color"
        absolute
        v-model="snackbar"
        :timeout="this.$store.state.toast.timeout"
        right
        top
      >
        <v-icon class="mr-2">mdi-check</v-icon>
        <span>{{ this.$store.state.toast.message }}</span>
        <template v-slot:action="{ attrs }">
          <v-btn color="white" text v-bind="attrs" @click="snackbar = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
      <!-- 토스트 메시지 끝 -->
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
import UserBoard from "/src/components/boards/UserBoard";

export default {
  components: {
    Board,
    ExcelBoard,
    UpdateBoard,
    UserBoard,
  },
  data: () => ({
    dialog: false,
    userDialog: false,
    excelDialog: false,
    updateDialog: false,
    selectedBoard: null,
  }),
  computed: {
    //선택된 컴포넌트 반환
    selectedComponent: function() {
      return Board;
    },
    color: {
      get() {
        return this.$store.getters.getColor;
      },
      set() {},
    },
    snackbar: {
      get() {
        return this.$store.getters.getSnackbar;
      },
      set(val) {
        this.$store.commit("setSnackbar", val);
      },
    },
    renderByUserType: function(){
      const userType = this.$store.state.userStore.userType;
      if(userType === "2" || userType === "") return false;
      return true;
    },
  },
  methods: {
    //유저 다이얼로그 열기
    openUserDialog() {
      (this.selectedBoard = UserBoard), (this.userDialog = true);
      this.dialog = this.userDialog;
    },
    //엑셀 다이얼로그 열기
    openExcelDialog() {
      (this.selectedBoard = ExcelBoard), (this.excelDialog = true);
      this.dialog = this.excelDialog;
    },
    //유저 다이얼로그 닫기
    closeUserDialog() {
      this.userDialog = false;
      this.dialog = this.userDialog;
    },
    //엑셀 다이얼로그 닫기
    closeExcelDialog() {
      this.excelDialog = false;
      this.dialog = this.excelDialog;
    },
    //수정 다이얼로그 열기
    openUpdateDialog() {
      (this.selectedBoard = UpdateBoard), (this.updateDialog = true);
      this.dialog = this.updateDialog;
    },
    //수정 다이얼로그 닫기
    closeUpdateDialog() {
      this.updateDialog = false;
      this.dialog = this.updateDialog;
    },
    //열린 다이얼로그에 따라 다이얼로그 닫기 함수 선택 제공
    closeDialog() {
      if (this.excelDialog) return this.closeExcelDialog();
      if (this.updateDialog) return this.closeUpdateDialog();
      if (this.userDialog) return this.closeUserDialog();
    },
    //로그아웃 버튼
    logout(){
      sessionStorage.clear();
      this.$router.push({name: "Login"});
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
  z-index: 100;
  border-bottom: 1px solid;
  background-color: white;
  
}


.logo-area{
  display: flex;
}
#logo{
  height: 50px;
  width:200px;
  display: flex;
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
#logout-btn{
  background-color: white;
  border: 1px solid;
  text-align: center;
}

#add-data-btn {
  background-color: white;
  border: 1px solid;
  text-align: center;
  margin-right: 8px;
}
#add-user-btn {
  background-color: white;
  border: 1px solid;
  text-align: center;
  margin-right: 8px;
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
  .logo-area{
  display: none;
 }

  .btn-text {
    display: none;
  }
}
</style>
