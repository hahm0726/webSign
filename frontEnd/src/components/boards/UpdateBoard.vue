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
        <v-btn id="close-btn" icon @click="closeUpdateDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </div>
    </header>
    <main class="contents-wrap">
      <v-data-table
        class="tables loaded-table"
        :search="search"
        no-data-text="데이터가 없습니다"
        no-results-text="일치하는 검색 결과가 없습니다"
        mobile-breakpoint="0"
        :headers="thItems"
        :items="totalData"
        :header-props="headerOption"
        hide-default-footer
        :footer-props="{itemsPerPage: -1,
                    'items-per-page-options':[-1]
                  }"
      >
        <template v-slot:top>
          <v-dialog v-model="signatureDialog" max-width="500px">
            <img-dialog
              @closeDialog="closeSignatureDialog"
              :item="selectedItem"
            ></img-dialog>
          </v-dialog>
          <div class="loaded-table-top">
            <div class="title-search-area">
              <div class="title-area">
                <div class="loaded-table-title table-title-text">
                  <span class="title-text">데이터 목록</span>
                  <v-icon class="title-icon" color="black">
                    mdi-file-document-outline
                  </v-icon>
                </div>
              </div>
              <div class="search-area">
               <v-icon>mdi-magnify</v-icon>
               <input id="search-input" type="text" placeholder="검색" :value="search" @input="inputSearch($event)"/>
              </div>
            </div>
            <div class="btn-group">
              <v-btn v-if="beforeCreate" id="table-add-btn" @click="addData">
                <span class="btn-text">데이터 추가</span>
                <v-icon class="icon-in-btn"> mdi-plus </v-icon>
              </v-btn>
              <v-btn v-else id="table-add-btn" color="success" @click="addConfirm">
                <span class="btn-text">추가 완료</span>
                <v-icon class="icon-in-btn"> mdi-check </v-icon>
              </v-btn>
              <v-btn
                id="save-to-db-btn"
                class="white--text"
                color="primary"
                :disabled="toUpdateData.length==0 && toDeleteData.length==0"
                @click="updateDb"
              >
                <span class="btn-text"> 수정 완료</span>
                <v-icon class="icon-in-btn"> mdi-database-plus </v-icon>
              </v-btn>
            </div>
          </div>
        </template>

        <template v-slot:[`item.idx`]="{ item }">
          <input
            class="idx-input"
            type="number"
            :value="item.idx"
            placeholder="입력 필수(중복X)"
            @keydown.tab="tabFunc($event)"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,'idx',item)"
          />
        </template>
        <template v-slot:[`item.name`]="{ item }">
          <input
            class="name-input"
            type="text"
            :value="item.name"
            @keydown.tab="tabFunc($event)"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,'name',item)"
          />
        </template>
        <template v-slot:[`item.birthDate`]="{ item }">
          <input
            class="birthDate-input"
            type="text"
            :value="item.birthDate"
            placeholder="yyyy-mm-dd"
            @keydown.tab="tabFunc($event)"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,'birthDate',item)"
          />
        </template>
        <template v-slot:[`item.location`]="{ item }">
          <input
            class="location-input"
            type="text"
            :value="item.location"
            @keydown.tab="tabFunc($event)"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,'location',item)"
          />
        </template>
        <template v-slot:[`item.amount`]="{ item }">
          <input
            class="amount-input"
            type="number"
            :value="item.amount"
            @keydown.tab="tabFunc($event)"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,'amount',item)"
          />
        </template>
        <template v-slot:[`item.receivedDate`]="{ item }">
          <input
            class="receivedDate-input"
            type="text"
            :value="item.receivedDate"
            placeholder="yyyy-mm-dd"
            @keydown.tab="tabFunc($event)"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,'receivedDate',item)"
          />
        </template>
        <template v-slot:[`item.signature`]="{ item }">
          <v-icon disabled v-if="item.signature == undefined"
            >mdi-file-cancel-outline
          </v-icon>
          <v-icon v-else @click="openSignatureDialog(item)">
            mdi-text-box-search-outline
          </v-icon>
        </template>
        <template v-slot:[`item.delete`]="{ item }">
          <v-icon @focus="$event.target.blur()" @click="deleteItem(item)">
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </main>
  </v-card>
</template>

<script>
import * as billApi from "/src/api/billApi";
import ImgDialog from "/src/components/dialog/ImgDialog";

export default {
  components: {
    ImgDialog,
  },
  data: () => ({
    search:"",
    snackbar:false,
    color:null,
    msg:null,
    headerOption: {
      "sort-icon": null,
    },
    thItems: [
      { text: "연번", value: "idx", sortable: true, align: "center" },
      { text: "이름", value: "name", sortable: true, align: "center" },
      {
        text: "생년월일",
        value: "birthDate",
        filterable: false,
        sortable: true,
        align: "center",
      },
      { text: "거주동", value: "location", sortable: true, align: "center" },
      { text: "수량", value: "amount", sortable: false, filterable: false, align: "center" },
      {
        text: "수령일",
        value: "receivedDate",
        sortable: false,
        align: "center",
      },
      { text: "서명", value: "signature", filterable: false, sortable: false, align: "center" },
      { text: "작업", value: "delete", filterable: false, sortable: false, align: "center" },
    ],
    toUpdateDataSet : new Set(),
    totalData: [],
    toDeleteData: [],
    toUpdateData: [],
    toCreateData: [],
    beforeCreate:true,
    beforeupdate:true,
    newData:{},
    signatureDialog: false,
    selectedItem: {},
  }),
  created() {
    this.getAllBill();
  },
  computed: {
    //수령날짜 출력 변환
    showReceivedDate: function(val) {
      if (val == null) return "수령 전";
      return val;
    },
    btnActivate:function(){
      
      if(this.toUpdateData.length !==0) return false
      if(this.toDeleteData.length !==0) return false

      return true;
    }
  },

  methods: {
    inputSearch(event){
      this.search=event.target.value;
    },
    callToast(msg,result){
      if (result === "success") {
        this.color="success";
        this.msg=msg;
      }
      //실패
      else if (result === "fail") {
        this.color="error";
        this.msg=msg;
      }
      this.snackbar=true;
    },
    //다이얼로그 닫기 동작
    closeUpdateDialog() {
      if(!this.btnActivate){
        if(confirm("데이터 수정이 완료되지 않았습니다. 그대로 닫겠습니까?")){
          this.$emit("closeDialog");
          this.initTempData();
          this.getAllBill();
        }
        return;
      }
      this.$emit("closeDialog");
    },
    //임시 데이터(삭제할 데이터, 업데이트할 데이터)를 빈값으로 초기화
    initTempData() {
      this.toDeleteData = [];
      this.toUpdateDataSet = new Set();
      this.toUpdateData = [];
      this.beforeupdate=true;
    },

    //읽은 엑셀데이터 테이블 비우기
    recoveryAllData() {
      this.getAllBill();
      this.initTempData();
    },
    //수령날짜 출력 변환
    receivedDate: function(val) {
      if (val == null) return "수령 전";
      return val;
    },

    //해당 데이터 행 삭제. 백엔드의 쉬운 처리를 위해 toDeleteData에 idx에 담기
    deleteItem(item) {
      const toDeleteItemIndex = this.totalData.indexOf(item);
      const toUpdateItemIndex = this.toUpdateData.indexOf(item);
      //새로 만든 아이템이 삭제되는 경우
      this.toUpdateData.splice(toUpdateItemIndex, 1);
      this.totalData.splice(toDeleteItemIndex, 1);

      if(item.id !== null){
        this.toDeleteData.push(item.id);
      }
      console.log(this.toUpdateData.length);
    },
    //모든 bill데이터 받아오기
    getAllBill() {
      billApi
        .getBillAll()
        .then((res) => {
          this.totalData = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    //서명 확인을 위한 서명 다이얼로그 열기
    openSignatureDialog(item) {
      this.selectedItem = item;
      this.signatureDialog = true;
    },
    //서명 확인을 위한 서명 다이얼로그 닫기
    closeSignatureDialog() {
      this.selectedItem = {};
      this.signatureDialog = false;
    },
    
    //연번 유효성 검증
    //1.빈 값 검사
    idxValidation(){
      const idxInputs = document.getElementsByClassName("idx-input");
      for (let i=0; i< idxInputs.length;i++){
        if(idxInputs[i].value == ""){
          alert("연번을 입력해주세요(숫자)");
          idxInputs[i].classList.add("validation-err");
          idxInputs[i].focus();
          return false;
        }
        idxInputs[i].classList.remove("validation-err");
      }
      return true;
    },
    //수정 완료 저장해 둔 임시 삭제 리스트와 테이블에 남은 모든 데이터 패치
    updateDb() {
      if(!this.idxValidation()){return;} 

      if(this.toUpdateData.length != 0){
        billApi
          .updateBillList(this.toUpdateData)
          .then(() => {
            this.getAllBill();
            this.callToast("수정완료","success");
          })
          .catch((err) => {
            this.callToast("수정실패","fail");
            console.log(err);
          });
      }
      if(this.toDeleteData.length != 0){
        billApi
          .deleteBillList(this.toDeleteData)
          .then(() => {
            this.callToast("수정 완료","success");
            this.getAllBill();
          })
          .catch((err) => {
            this.callToast("수정실패","fail");
            console.log(err);
          });
      }
      
      this.initTempData();
    },
    //입력받은 값 중복 체크
    isDuplicated (val,inputName,item){
      for(var i=0; i<this.totalData.length;i++){
        if(item === this.totalData[i]) continue; //자기 자신의 값인 경우 중복X
        if(val == this.totalData[i][inputName]){
          return true;
        }
      }
      return false;
    },
    //blurEvent 처리함수
    blurFunc(event,inputName,item){
      const inputedValue = event.target.value;
      //idx-input에서 blur가 발생한 경우
      if(inputName == "idx"){
        if(this.isDuplicated(inputedValue,inputName,item)){
          event.target.classList.add("duplicated-err");
          alert(`해당 연번 ${inputName}이 이미 존재합니다.`);
          event.target.focus();
          event.target.value=null;
          return false;
        } 
        event.target.classList.remove("duplicated-err");
      }
      event.target.classList.remove("validation-err");

      this.addToUpdateData(item);

      this.beforeupdate=false;
      this.inputVal(inputName,inputedValue,item);
    },

    //데이터 input handler
    inputVal(inputName,inputedVal, item) {
      console.log(item);
      item[inputName] = inputedVal;
    },

    addToUpdateData(item){
      const prevSetLen = this.toUpdateDataSet.size;
      this.toUpdateDataSet.add(item);
      if(prevSetLen !== this.toUpdateDataSet.size){
        this.toUpdateData.push(item);
      }
    },

    tabFunc(event){
      if(!event.target.blur()){event.preventDefault();}
    },


    //이름 유효성 검사
    validateName(val) {
      if (val == null || val == undefined || val == "") {
        val=null
      }
      return val;
    },

    //생년월일 유효성 검사
    validateBirthDate(val) {
       if (val == null || val == undefined || val == "") {
        val=""
      }
      return val;
    },

    //이름 유효성 검사
    validateLocation(val) {
       if (val == null || val == undefined || val == "") {
        val=null
      }
      return val;
    },
    //이름 유효성 검사
    validateAmount(val) {
       if (val == null || val == undefined || val == "") {
        val=null
      }
      return val;
    },
    //생년월일 유효성 검사
    validateReceivedDate(val) {
       if (val == null || val == undefined || val == "") {
        val=null
      }
      return val;
    },
  
    //연번 유효성 검사
    validateIdx(val) {
      if (val == null || val == undefined || val == "") {
        return false;
      }
      return true;
    },

    isValid(){
      const Row = document.querySelector(".loaded-table tbody");
      console.log(Row);
      /*
      const idx = document.getElementsByClassName(".idx-input");
      const name = document.getElementsByClassName(".name-input");
      const location = document.getElementsByClassName(".location-input");
      const amount = document.getElementsByClassName(".amount-input");
      const birthDate = document.getElementsByClassName(".birthDate-input");
      const receivedDate = document.getElementsByClassName(".receivedDate-input");
      */

    },
    
    //데이터 한 행 추가
    addData() {
      let newData = {
        id:null,
        idx:null,
        name:null,
        birthDate:null,
        location:null,
        amount:null,
        receivedDate:null,
        signature:null,
      };
      this.totalData.unshift(newData);
      this.addToUpdateData(this.totalData[0]);
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
#file-input {
  border: 2px solid;
  border-radius: 5px;
  padding-left: 2px;
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
  margin-bottom: 16px;
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
#table-clear-btn {
  margin-right: 8px;
  text-align: center;
}
#save-to-db-btn {
  text-align: center;
}

.title-area {
  width: fit-content;
  padding-bottom: 8px;
  border-bottom: 3px solid skyblue;
}
.loaded-table-title {
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
.loaded-table input[type="text"] {
  width: 100%;
}
.loaded-table input[type="number"] {
  width: 30%;
}
.input-idx {
  width: 100% !important;
}
.loaded-table input[type="number"]::-webkit-outer-spin-button,
.loaded-table input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.validation-err{
  outline:2px solid red;
  border-radius: 2px;
}
.duplicated-err{
  outline:2px solid red;
  border-radius: 2px;
}

.v-data-table::v-deep div.v-data-footer{
  justify-content: flex-end !important;
}
@media screen and (max-width: 600px) {
  #file-input {
    border: 2px solid;
    border-radius: 5px;
    padding-left: 2px;
    width: 180px;
    font-size: 10px;
  }

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
  #table-clear-btn {
    margin-right: 8px;
    text-align: center;
    width: fit-content;
  }

  #save-to-db-btn {
    text-align: center;
    width: fit-content;
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
