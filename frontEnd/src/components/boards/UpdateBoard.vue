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
        mobile-breakpoint="0"
        :no-data-text="noDataText"
        :headers="thItems"
        :items="totalData"
        :header-props="headerOption"
        :footer-props="{itemsPerPage: 10,
                    'items-per-page-options':[10]
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
            <div class="loaded-table-title-area">
              <div class="loaded-table-title table-title-text">
                <span class="title-text">데이터 목록</span>
                <v-icon class="title-icon" color="black">
                  mdi-file-document-outline
                </v-icon>
              </div>
            </div>
            <div class="btn-group">
              <v-btn id="table-add-btn" color="success" @click="addData">
                <span class="btn-text">데이터 추가</span>
                <v-icon class="icon-in-btn"> mdi-plus </v-icon>
              </v-btn>
              <v-btn
                id="table-clear-btn"
                color="error"
                :disabled="btnActivate"
                @click="recoveryAllData"
              >
                <span class="btn-text">데이터 되돌리기</span>
                <v-icon class="icon-in-btn"> mdi-sync </v-icon>
              </v-btn>
              <v-btn
                id="save-to-db-btn"
                class="white--text"
                color="primary"
                :disabled="btnActivate"
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
            class="input-idx"
            type="number"
            :value="item.idx"
            placeholder="입력 필수(중복X)"
            @keydown.tab="tabFunc($event,item,isIdxDuplicated)"
            @keyup.enter="isIdxDuplicated($event,item)"
            @blur="blurFunc($event,item,item.idx,updateIdx)"
          />
        </template>
        <template v-slot:[`item.name`]="{ item }">
          <input
            type="text"
            :value="item.name"
            @keydown.tab="tabFunc($event)"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,item,item.name,updateName)"
          />
        </template>
        <template v-slot:[`item.birthDate`]="{ item }">
          <input
            type="text"
            :value="item.birthDate"
            placeholder="yyyy-mm-dd"
            @keydown.tab="tabFunc($event)"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,item,item.birthDate,updateBirthDate)"
          />
        </template>
        <template v-slot:[`item.location`]="{ item }">
          <input
            type="text"
            :value="item.location"
            @keydown.tab="tabFunc($event)"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,item,item.location,updateLocation)"
          />
        </template>
        <template v-slot:[`item.amount`]="{ item }">
          <input
            type="number"
            :value="item.amount"
            @keydown.tab="tabFunc($event)"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,item,item.amount,updateAmount)"
          />
        </template>
        <template v-slot:[`item.receivedDate`]="{ item }">
          <input
            type="text"
            :value="item.receivedDate"
            placeholder="yyyy-mm-dd"
            @keydown.tab="tabFunc($event)"
            @keyup.enter="$event.target.blur()"
            @blur="blurFunc($event,item,item.receivedDate,updateReceivedDate)"
          />
        </template>
        <template v-slot:[`item.signature`]="{ item }">
          <v-icon disabled v-if="item.signature == undefined"
            >mdi-file-cancel-outline</v-icon
          >
          <v-icon v-else @focus="$event.target.blur()" @click="openSignatureDialog(item)">
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
    snackbar:false,
    color:null,
    msg:null,
    headerOption: {
      "sort-icon": null,
    },
    noDataText: "아직 불러온 데이터가 없습니다",
    thItems: [
      { text: "연번", value: "idx", sortable: true, align: "center" },
      { text: "이름", value: "name", sortable: true, align: "center" },
      {
        text: "생년월일",
        value: "birthDate",
        sortable: true,
        align: "center",
      },
      { text: "거주동", value: "location", sortable: true, align: "center" },
      { text: "수량", value: "amount", sortable: false, align: "center" },
      {
        text: "수령일",
        value: "receivedDate",
        sortable: false,
        align: "center",
      },
      { text: "서명", value: "signature", sortable: false, align: "center" },
      { text: "삭제", value: "delete", sortable: false, align: "center" },
    ],
    totalData: [],
    toDeleteData: [],
    toUpdateData: [],
    toCreateData: [],
    toUpdateDataSet: new Set(),
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
      if(this.toCreateData.length !==0) return false

      return true;
    }
  },

  methods: {
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
      this.toUpdateData = [];
      this.toCreateData = [];
      this.toUpdateDataSet = new Set();
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
      const toCreateItemIndex = this.toCreateData.indexOf(item);
      const toUpdateItemIndex = this.toUpdateData.indexOf(item);
      //새로 만든 아이템이 삭제되는 경우
      if(toCreateItemIndex !== -1){
        this.toCreateData.splice(toCreateItemIndex, 1);
        this.toUpdateData.splice(toUpdateItemIndex, 1);
      }
      //기존에 존제하던 아이템 삭제
      else{
        //기존에 존재하던 아이템 중 업데이트 중 지운 경우
        if(toUpdateItemIndex !== -1){
          this.toUpdateData.splice(toUpdateItemIndex, 1);
        }
        this.toDeleteData.push(item.id);
      }
      this.totalData.splice(toDeleteItemIndex, 1);
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
      const idxInputs = document.getElementsByClassName("input-idx");
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
        console.log(this.toUpdateData);
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
    //idx-input 엔터로 입력 완료 시 연번 중복 확인 중복
    isIdxDuplicated (event,item){
      const inputedVal= event.target.value;
      for(var i=0; i<this.totalData.length;i++){
        //새로 생성되는 데이터를 위해 널값은 중복으로 감지 X
        if(inputedVal===null || inputedVal==="") continue;
        if(item === this.totalData[i]) continue; //자기 자신의 값인 경우 중복X
        if(inputedVal == this.totalData[i].idx){
          event.target.focus();
          event.target.value=null;
          event.target.classList.add("duplicated-err");
          alert(`해당 연번 ${inputedVal}이 이미 존재합니다.`); 
          return false;
        }
      }
      event.target.classList.remove("duplicated-err");
      event.target.classList.remove("validation-err");
      //기존의 데이터 값과 변경된 값이 같으면 굳이 업데이트 목록에 추가X
      event.target.blur(event,item); 
       return true;
    },
    tabFunc(event,item,validate){
      if(validate===undefined){event.target.blur(); return;}
      if(!validate(event,item)){
        event.preventDefault();
      }
    },
    //blurEvent 처리함수
    blurFunc(event,item,origin,updateFunc){
      const inputedValue = event.target.value;
      //event가 key.up enter로 blur처리된 경우
      if(event.relatedTarget===null){
        //입력된 값이 기존의 데이터 연번과 같을 경우 업데이트 목록 추가X
        if(inputedValue == origin){return;}
        updateFunc(inputedValue,item);
        return;
      }
      //key.up enter로 blur 처리되지 않은 경우
      event.target.value = origin;
    },

    //연번 데이터 수정 input handler
    updateIdx(inputedVal,item) {
      
      item.idx = inputedVal;
      const prevLen = this.toUpdateDataSet.size;
      if(this.toUpdateDataSet.add(item).size !=prevLen){
        this.toUpdateData.push(item);
      }
    },
    //이름 데이터 수정 input handler
    updateName(inputedVal, item) {
      item.name = inputedVal;
      const prevLen = this.toUpdateDataSet.size;
      if(this.toUpdateDataSet.add(item).size !=prevLen){
        this.toUpdateData.push(item);
      }
    },
    //생년월일 데이터 수정 input handler
    updateBirthDate(inputedVal, item) {
      if(inputedVal==="" && item.birthDate==null){return;}
      item.birthDate = inputedVal;
      const prevLen = this.toUpdateDataSet.size;
      if(this.toUpdateDataSet.add(item).size !=prevLen){
        this.toUpdateData.push(item);
      }
    },
    //거주동 데이터 수정 input handler
    updateLocation(inputedVal, item) {
      if(inputedVal==="" && item.location==null){return;}
      item.location = inputedVal;
      const prevLen = this.toUpdateDataSet.size;
      if(this.toUpdateDataSet.add(item).size !=prevLen){
        this.toUpdateData.push(item);
      }
    },
    //수량 데이터 수정 input handler
    updateAmount(inputedVal, item) {
      if(inputedVal==="" && item.amount==null){return;}
      item.amount = inputedVal;
      const prevLen = this.toUpdateDataSet.size;
      if(this.toUpdateDataSet.add(item).size !=prevLen){
        this.toUpdateData.push(item);
      }
    },
    //수령일 데이터 수정 input handler
    updateReceivedDate(inputedVal, item) {
      if(inputedVal==="" && item.receivedDate==null){return;}
      item.receivedDate = inputedVal;
      const prevLen = this.toUpdateDataSet.size;
      if(this.toUpdateDataSet.add(item).size !=prevLen){
        this.toUpdateData.push(item);
      }
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
      this.toCreateData.push(newData);
      this.totalData.unshift(newData);
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
  justify-content: center !important;
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
