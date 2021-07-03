<template>
  <v-card>
    <!-- 토스트 메시지 -->
      <v-snackbar
        absolute
        :color="color"
        v-model="snackbar"
        timeout="2000"
        right
        top
      >
        <v-icon class="mr-2">mdi-check</v-icon>
        <span>{{msg}}</span>
        <template v-slot:action="{ attrs }">
          <v-btn color="white" text v-bind="attrs" @click="snackbar = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
      <!-- 토스트 메시지 끝 -->
    <header id="dialog-header">
      <div class="dialog-header-wrap">
        <v-spacer></v-spacer>
        <v-btn id="close-btn" icon @click="closeUserDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </div>
    </header>
    <main class="contents-wrap">
      <v-data-table
        class="tables loaded-table"
        mobile-breakpoint="0"
        :no-data-text="noDataText"
        :headers="thItems"
        :items="totalUser"
        :header-props="headerOption"
        hide-default-footer
      >
        <template v-slot:top>
          <div class="loaded-table-top">
            <div class="loaded-table-title-area">
              <div class="loaded-table-title table-title-text">
                <span class="title-text">사용자 목록</span>
                <v-icon class="title-icon" color="black">
                  mdi-account-multiple
                </v-icon>
              </div>
            </div>
            <div class="btn-group">
              <v-btn id="table-add-btn" color="success" @click="addUser">
                <span class="btn-text">사용자 추가</span>
                <v-icon class="icon-in-btn"> mdi-plus </v-icon>
              </v-btn>
            </div>
          </div>
        </template>

        <template v-slot:[`item.department`]="{ item }">
          <input :disabled="!item.hasOwnProperty('beforeSave')" class="department-input" type="text" :value="item.department" placeholder="(부서 입력)"/>
        </template>
        <template v-slot:[`item.name`]="{ item }">
          <input :disabled="!item.hasOwnProperty('beforeSave')" class="name-input" type="text" :value="item.name" placeholder="(이름 입력)"/>
        </template>
        <template v-slot:[`item.username`]="{ item }">
          <input :disabled="!item.hasOwnProperty('beforeSave')" class="username-input" type="text" :value="item.username" placeholder="(아이디 입력)"/>
        </template>
        <template v-slot:[`item.password`]="{ item }">
          <input :disabled="!item.hasOwnProperty('beforeSave')" class="password-input" type="password" :value="item.password" placeholder="(비밀번호 입력)"/>
        </template>
        <template v-slot:[`item.userType`]="{ item }">
          <!--유저타입-->
          <select :disabled="!item.hasOwnProperty('beforeSave')" class="userType-select" v-model="item.userType">
            <option disabled value="">권한선택</option>
            <option value="1">관리자</option>
            <option value="2">일반</option>
          </select>
        </template>
        <template v-slot:[`item.action`]="{ item }">
          <v-icon v-if="item.beforeSave" class="mr-2" color="success" @click="saveItem(item)">
            mdi-check
          </v-icon>
          <v-icon color="error" @click="deleteItem(item)">
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </main>
  </v-card>
</template>

<script>

export default {
  data: () => ({
    snackbar:false,
    color:null,
    msg:null,
    headerOption: {
      "sort-icon": null,
    },
    noDataText: "아직 불러온 데이터가 없습니다",
    thItems: [
      { text: "부서", value: "department", sortable: true, align: "center" },
      { text: "이름", value: "name", sortable: true, align: "center" },
      { text: "아이디", value: "username", sortable: false, align: "center" },
      { text: "패스워드", value: "password", sortable: false, align: "center" },
      { text: "권한", value: "userType", sortable: false, align: "center" },
      { text: "작업", value: "action", sortable: false, align: "center" },
    ],
    totalUser:[
      {
        id:1,
        company:null,
        userType:2,
        department:"환경",
        name:"홍길동",
        username:"hsh07260",
        password:"@@hsh07260",
      },
      {
        id:2,
        company:null,
        userType:2,
        department:"환경",
        name:"최길자",
        username:"abc07260",
        password:"1234",
      },
      {
        id:3,
        company:null,
        userType:2,
        department:"환경",
        name:"홍길동",
        username:"hsh07260",
        password:"fasdf",
      },
    ],
  }),

  methods: {
    closeUserDialog(){
      this.$emit("closeDialog");
    },
    callToast(msg,result){
      this.snackbar=false;
      if (result === "success") {
        this.color="success";
        this.msg=msg;
      }
      //실패
      else if (result === "fail") {
        this.color="success";
        this.msg=msg;
      }
      this.snackbar=true;
    },
    validate_department(val){
      console.log(val);
      if(val==null || val==undefined || val==""){
        alert("부서를 입력해주세요");
        return false;
      }
      return true;
    },
    validate_name(val){
      if(val==null || val==undefined || val==""){
        console.log("aaaa");
        alert("이름을 입력해주세요");
        return false;
      }
      return true;
    },
    validate_username(val){
      if(val==null || val==undefined || val==""){
        alert("아이디를 입력해주세요");
        return false;
      }
      return true;
    },
    validate_password(val){
      if(val==null || val==undefined || val==""){
        alert("비밀번호를 입력해주세요");
        return false;
      }
      return true;
    },

    isValid(event){
      const tr = event.target.parentNode.parentNode;
      const department = tr.getElementsByClassName("department-input");
      const name = tr.getElementsByClassName("name-input");
      const username = tr.getElementsByClassName("username-input");
      const password = tr.getElementsByClassName("password-input");
      //const userType = tr.getElementsByClassName("userType-select");

      if(this.validate_department(department.value)){
        department.classList.add("validation-err");
        department.focus();
        return false;
      }
      if(!this.validate_name(name.value)){
        name.classList.add("validation-err");
        name.focus();
        return false;
      }
      if(!this.validate_username(username.value)){
        username.classList.add("validation-err");
        username.focus();
        return false;
      }
      if(!this.validate_password(password.value)){
        password.classList.add("validation-err");
        password.focus();
        return false;
      }
      department.classList.remove("validation-err");
      name.classList.remove("validation-err");
      username.classList.remove("validation-err");
      password.classList.remove("validation-err");
      return true;
    },
    saveItem(item){
       if(confirm("해당 유저를 저장하시겠습니까?")){
        item.beforeSave=false;
        delete item.beforeSave; 
        //axios create 코드
        this.callToast("사용자 생성 완료","success");
      }
    },
    //해당 데이터 행 삭제. 백엔드의 쉬운 처리를 위해 toDeleteData에 idx에 담기
    deleteItem(item) {
      if(confirm("해당 유저를 삭제하시겠습니까?")){
        const toDeleteItemIndex = this.totalUser.indexOf(item);
        this.totalUser.splice(toDeleteItemIndex, 1);
        if(!Object.prototype.hasOwnProperty.call(item,"beforeSave")){
          //axios delete 코드
          this.callToast("사용자 삭제 완료","success");
        }
      }
      
    },
   
   
    //데이터 한 행 추가
    addUser() {
      let newUser = {
        id:null,
        department:null,
        name:null,
        username:null,
        password:null,
        userType:"",
        beforeSave:true,
        };
      this.totalUser.unshift(newUser);
    },
  },
};
</script>

<style scoped>
#dialog-header {
  border: 2px solid black;
  padding: 0;
}
.dialog-header-wrap {
  margin: 0;
  padding-left: 8px;
  padding-right: 8px;
  display: flex;
  align-items: center;
  height: 60px;
}

#close-btn {
  color: black;
  text-align: center;
}

.contents-wrap {
  min-height: 90vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.tables {
  width: 100%;
  max-width: 1200px;
}
.loaded-table {
  margin-top: 16px;
}
.loaded-table-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
#table-add-btn {
  margin-right: 8px;
  text-align: center;
}
.loaded-table-title-area {
  width: fit-content;
  padding-bottom: 8px;
  border-bottom: 3px solid skyblue;
}
.loaded-table-title {
  display: flex;
  align-items: center;
  justify-content: center;
}
.table-title-text {
  font-size: 24px;
  font-weight: bold;
}
.title-icon {
  align-self: flex-end;
  padding-left: 15px;
  padding-right: 15px;
}
.btn-group {
  display: flex;
}

.btn-text {
  display: initial;
}
.icon-in-btn {
  display: none;
}

.loaded-table input {
  text-align: center;
}
.loaded-table input[type="text"],
.loaded-table select {
  width: 100%;
}

.loaded-table select{
  text-align-last: center;
  text-align: center;
  -ms-text-align-last: center;
  -moz-text-align-last: center;
}


.validation-err{
  outline:2px solid red;
  border-radius: 2px;
}
.duplicated-err{
  outline:2px solid red;
  border-radius: 2px;
}

@media screen and (max-width: 600px) {

  .btn-group {
    display: flex;
    margin-right: 8px;
  }
  .btn-text {
    display: none;
  }
  .icon-in-btn {
    display: initial;
  }
  .btn-group button.v-btn {
    min-width: 0;
    padding: 10px;
  }

  .table-title-text {
    font-size: 16px;
    font-style: bold;
  }
}

.before-sign {
  font-size: 1px;
}
/*제일 작은 모바일 사이즈(세로) */
@media screen and (max-width: 465px) {
  .v-data-table::v-deep th {
    font-size: 2px !important;
    text-align: center;
    padding: 1px !important;
  }
  .v-data-table::v-deep td {
    font-size: 1px !important;
    padding: 1px !important;
  }
}
/*제일 작은 모바일 사이즈(가로) */
@media screen and (min-width: 465px) and (max-width: 600px) {
  .v-data-table::v-deep th {
    font-size: 2px !important;
    text-align: center;
    padding: 1px !important;
  }
  .v-data-table::v-deep td {
    font-size: 1px !important;
    padding: 1px !important;
  }
}
</style>
