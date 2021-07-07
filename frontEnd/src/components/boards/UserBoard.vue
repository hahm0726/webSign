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
      <span>{{ msg }}</span>
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
        class="tables user-table"
        :search="search"
        no-data-text="데이터가 없습니다"
        no-results-text="일치하는 검색 결과가 없습니다"
        mobile-breakpoint="0"
        :headers="thItems"
        :items="totalUser"
        :header-props="headerOption"
        :footer-props="{itemsPerPage: 10,
                    'items-per-page-options':[10]
                  }"
      >
        <template v-slot:top>
          <div class="user-table-top">
            <div class="title-search-area">
              <div class="title-area">
                <div class="user-table-title table-title-text">
                  <span class="title-text">사용자 목록</span>
                  <v-icon class="title-icon" color="black">
                    mdi-account-multiple
                  </v-icon>
                </div>
              </div>
              <div class="search-area">
                <v-icon>mdi-magnify</v-icon>
                <input id="search-input" type="text" placeholder="검색" :value="search" @input="inputSearch($event)"/>
              </div>
            </div>
            <div class="btn-group">
              <v-btn id="table-add-btn" color="success" v-if="beforeCreate" @click="createUser">
                <span class="btn-text">사용자 생성</span>
                <v-icon class="icon-in-btn"> mdi-plus </v-icon>
              </v-btn>
              <v-btn id="table-add-btn" color="primary" v-else @click="saveItem">
                <span class="btn-text">생성 완료</span>
                <v-icon class="icon-in-btn"> mdi-check </v-icon>
              </v-btn>
            </div>
          </div>
        </template>

        <template v-slot:[`item.department`]="{ item }">
          <input
            :disabled="item !== newUser"
            class="department-input"
            type="text"
            :value="item.department"
            @input="inputFunc($event)"
            @keydown.tab="$event.target.blur()"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,'department',item)"
            :placeholder="placehorderFunc('(부서 입력)',item)"
          />
        </template>
        <template v-slot:[`item.name`]="{ item }">
          <input
            :disabled="item !== newUser"
            class="name-input"
            type="text"
            :value="item.name"
            @input="inputFunc($event)"
            @keydown.tab="$event.target.blur()"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,'name',item)"
            :placeholder="placehorderFunc('(이름 입력)',item)"
          />
        </template>
        <template v-slot:[`item.username`]="{ item }">
          <input
            :disabled="item !== newUser"
            class="username-input"
            type="text"
            :value="item.username"
            @input="inputFunc($event)"
            @keydown.tab="$event.target.blur()"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,'username',item)"
            :placeholder="placehorderFunc('(아이디 입력)',item)"
          />
        </template>
        <template v-slot:[`item.password`]="{ item }">
          <input
            :disabled="item !== newUser"
            class="password-input"
            type="password"
            :value="item.password"
            @input="inputFunc($event)"
            @keydown.tab="$event.target.blur()"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,'password',item)"
            :placeholder="placehorderFunc('(비밀번호 입력)',item)"
          />
        </template>
        <template v-slot:[`item.userType`]="{ item }">
          <!--유저타입-->
          <select
            :disabled="selectDisabled(item)"
            class="userType-select"
            v-model="item.userType"
            @change="updateUserType(item)"
          >
            <option disabled value="">권한선택</option>
            <option value="1">관리자</option>
            <option value="2">일반</option>
          </select>
        </template>
        <template v-slot:[`item.action`]="{ item }">
          <v-icon v-if="item.userType !=='0'" 
                  color="error" 
                  @click="deleteItem(item)"
          >
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </main>
  </v-card>
</template>

<script>
import * as userApi from "/src/api/userApi";

export default {
  data: () => ({

    beforeCreate: true,
    snackbar: false,
    color: null,
    msg: null,
    search:"",
    newUser:{},
    headerOption: {
      "sort-icon": null,
    },
    noDataText: "아직 불러온 데이터가 없습니다",
    thItems: [
      { text: "부서", value: "department", sortable: true, align: "center" },
      { text: "이름", value: "name", sortable: true, align: "center" },
      { text: "아이디", value: "username", filterable: false, sortable: false, align: "center" },
      { text: "패스워드", value: "password", filterable: false, sortable: false, align: "center" },
      { text: "권한", value: "userType", filterable: false, sortable: false, align: "center" },
      { text: "작업", value: "action", filterable: false, sortable: false, align: "center" },
    ],
    totalUser: [],
  }),
  created(){
    this.getAllUser();
  },
  methods: {
    inputSearch(event){
      this.search=event.target.value;
    },
    placehorderFunc(text,item){
      if(item===this.newUser){
        return text;
      }
    },
    //select 사용 가능 여부 처리 함수
    selectDisabled(item){
      if(!this.beforeCreate && item === this.newUser) return false;
      //새로운 유저 생성 전 이거나 유저타입이 슈퍼유저가 아닌 경우
      if(this.beforeCreate && item.userType !== '0')return false;
      return true;
    },

    //유저타입값 변경에 의한 데이터 변경 axios
    updateUserType(item){
      if(item===this.newUser){return;}
      const data = {userType:item.userType};
      userApi
          .updateUser(item.id,data)
          .then(() => {
            this.callToast("권한 변경 완료", "success");
          })
          .catch((err) => {
            this.callToast("권한 변경 실패", "fail");
            console.log(err.response);
          });
    },
    closeUserDialog() {
      this.$emit("closeDialog");
    },
    callToast(msg, result) {
      this.snackbar = false;
      if (result === "success") {
        this.color = "success";
        this.msg = msg;
      }
      //실패
      else if (result === "fail") {
        this.color = "error";
        this.msg = msg;
      }
      this.snackbar = true;
    },

    inputFunc(event){
      event.target.classList.remove("validation-err");
    },  
    /*
    blurEvent 처리함수
    inputName:입력받는 속성
    item: 해당 item 객체
    origin: 해당 속성의 원본값
    */
    blurFunc(event,inputName,item){
      const inputedValue = event.target.value;
      this.inputVal(inputName,inputedValue,item);
    },

    //데이터 input handler
    inputVal(inputName,inputedVal, item) {
      item[inputName] = inputedVal;
    },

    //부서 유효성 검사
    validate_department(val) {
      if (val == null || val == undefined || val == "") {
        alert("부서를 입력해주세요");
        return false;
      }
      return true;
    },

    //이름 유효성 검사
    validate_name(val) {
      if (val == null || val == undefined || val == "") {
        alert("이름을 입력해주세요");
        return false;
      }
      return true;
    },

    //아이디 유효성 검사
    async validate_username(val) {
      if (val == null || val == undefined || val == "") {
        alert("아이디를 입력해주세요");
        return false;
      }
      var idPattern = new RegExp('[^a-zA-Z0-9]'); //아이디 패턴검사식

      if (idPattern.test(val)) {
        alert("아이디를 영문자와 숫자로 입력해 주세요.");
        return false;
      }

      //아이디 중복 검사
      userApi.isUserNameDuplicated(val)
      .then((res)=>{
        if(res.data.state==="1"){
          alert("이미 사용중인 아이디 입니다.");
          return false;
        }
      })
      .catch(()=>{
      })

      return true;
    },

    //비밀번호 유효성 검사
    validate_password(val) {
      if (val == null || val == undefined || val == "") {
        alert("비밀번호를 입력해주세요");
        return false;
      }
      return true;
    },

    async isValid() {
      const department = document.querySelector(".department-input");
      const name = document.querySelector(".name-input");
      const username = document.querySelector(".username-input");
      const password = document.querySelector(".password-input");

      //부서 유효성 검사
      if (!this.validate_department(department.value)) {
        department.classList.add("validation-err");
        department.focus();
        return false;
      }
      //이름 유효성 검사
      else if (!this.validate_name(name.value)) {
        name.classList.add("validation-err");
        name.focus();
        return false;
      }
      //아이디 유효성 검사
      else if (!await this.validate_username(username.value)) {
        username.classList.add("validation-err");
        username.focus();
        return false;
      }
      //비밀번호 유효성 검사
      else if (!this.validate_password(password.value)) {
        password.classList.add("validation-err");
        password.focus();
        return false;
      }
      
      return true;
    },
    getAllUser(){
      userApi
          .getUsers()
          .then((res) => {
            this.totalUser=res.data;
          })
          .catch((err) => {
            console.log(err.response);
          });
    },
    async saveItem() {
      if (confirm("해당 유저를 저장하시겠습니까?")) {
        const validState = await this.isValid();
        if(validState) {
          //axios create 코드
          userApi
            .createUser(this.newUser)
            .then(() => {
              this.beforeCreate = true;
              this.getAllUser();
              this.callToast("사용자 생성 완료", "success");
            })
            .catch((err) => {
              this.callToast("사용자 생성 실패", "fail");
              console.log(err.response);
            });
          }
      }
    },
    //해당 데이터 행 삭제. 백엔드의 쉬운 처리를 위해 toDeleteData에 idx에 담기
    deleteItem(item) {
      if (confirm("해당 유저를 삭제하시겠습니까?")) {
        const toDeleteItemIndex = this.totalUser.indexOf(item);
        //axios delete 코드
        if (item !== this.newUser) {
          userApi
          .deleteUser(item.id)
          .then(() => {
            this.beforeCreate = true;
            this.getAllUser();
            this.callToast("사용자 삭제 완료", "success");
          })
          .catch((err) => {
            console.log(err.response);
            this.callToast("사용자 삭제 실패", "fail");
          });
        }else{
          this.beforeCreate=true;
          this.totalUser.splice(toDeleteItemIndex, 1);
          this.callToast("사용자 삭제 완료", "success");
        }
      }
    },
    //유저생성
    createUser() {
      this.newUser = {
        department: null,
        name: null,
        username: null,
        password: null,
        userType: "",
        company:null,
      };
      this.beforeCreate=false;
      this.totalUser.unshift(this.newUser);
    },
  }
};
</script>

<style scoped>
#dialog-header {
  padding: 0;
  margin-bottom: 0;
}
.dialog-header-wrap {
  margin: 0;
  padding-left: 8px;
  padding-right: 8px;
  display: flex;
  align-items: center;
  height: 50px;
  border-bottom: 1px solid;
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
.user-table {
  margin-top: 16px;
}
.user-table-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
#table-add-btn {
  margin-right: 8px;
  text-align: center;
}
.title-area {
  width: fit-content;
  padding-bottom: 8px;
  border-bottom: 3px solid skyblue;
}


.user-table-title {
  display: flex;
  align-items: center;
  justify-content: center;
}
.search-area{
  margin-top: 8px;
  display: flex;
  align-items: center;
  height: fit-content;
  outline: 1px solid black;
}
#search-input{
  width:300px;
  padding-left: 4px;
  text-align: initial;
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

.user-table input {
  text-align: center;
}
.user-table input[type="text"],
.user-table select {
  width: 100%;
}

.user-table select {
  text-align-last: center;
  text-align: center;
  -ms-text-align-last: center;
  -moz-text-align-last: center;
}

.v-data-table::v-deep div.v-data-footer{
  justify-content: flex-end !important;
}

.validation-err {
  outline: 2px solid red;
  border-radius: 2px;
}
.duplicated-err {
  outline: 2px solid red;
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
  #search-input{
    font-size: 12px;
    width:150px;
  }
  .v-data-table::v-deep th {
    font-size: 16px !important;
    text-align: center;
    padding: 1px !important;
  }
  .v-data-table::v-deep td {
    font-size: 12px !important;
    padding: 1px !important;
  }
}
/*제일 작은 모바일 사이즈(가로) */
@media screen and (min-width: 465px) and (max-width: 600px) {
  .v-data-table::v-deep th {
    font-size: 16px !important;
    text-align: center;
    padding: 1px !important;
  }
  .v-data-table::v-deep td {
    font-size: 12px !important;
    padding: 1px !important;
  }
}
</style>
