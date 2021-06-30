<template>
  <v-card>
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
        hide-default-footer
        :header-props="headerOption"
      >
        <template v-slot:top>
            <v-dialog v-model="signatureDialog" max-width="500px">
        <v-card class="pa-2">
          <v-card-actions class="pa-0">
            <v-spacer></v-spacer>
            <v-btn small @click="closeSignatureDialog">
              닫기
            </v-btn>
            <v-btn color="error" small>
              서명삭제
            </v-btn>
          </v-card-actions>
        </v-card>
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
                <v-btn id="table-add-btn" color="success">
                    <span class="btn-text">데이터 추가</span>
                    <v-icon class="icon-in-btn"> mdi-plus </v-icon>
                </v-btn>
              <v-btn
                id="table-clear-btn"
                color="error"
                @click="recoveryAllData"
              >
                <span class="btn-text">데이터 되돌리기</span>
                <v-icon class="icon-in-btn"> mdi-sync </v-icon>
              </v-btn>
              <v-btn
                id="save-to-db-btn"
                class="white--text"
                color="primary"
                @click="updateDb"
              >
                <span class="btn-text"> 수정 완료</span>
                <v-icon class="icon-in-btn"> mdi-database-plus </v-icon>
              </v-btn>
            </div>
          </div>
        </template>

        <template v-slot:[`item.idx`]="{item}">
          <input :id="item.idx + '_idx'"
                 class="input-idx"
                 type="number"
                 :value="item.idx"
                 placeholder="입력 필수(중복X)"
                 @input="updateIdx($event,item)">
        </template>
        <template v-slot:[`item.name`]="{item}">
          <input :id="item.idx + '_name'" type="text" :value="item.name" @input="updateName($event,item)">
        </template>
        <template v-slot:[`item.birthDate`]="{item}">
          <input :id="item.idx + 'birthDate'"
                 type="text" :value="item.birthDate" 
                 placeholder="yyyy-mm-dd"
                 @input="updateBirthDate($event,item)">
        </template>
        <template v-slot:[`item.location`]="{item}">
          <input :id="item.idx + '_location'" type="text" :value="item.location" @input="updateLocation($event,item)">
        </template>
        <template v-slot:[`item.amount`]="{item}">
          <input :id="item.idx + '_amount'" type="number" :value="item.amount" @input="updateAmount($event,item)">
        </template>
        <template v-slot:[`item.receivedDate`]="{ item }">
          <input :id="item.idx + '_receivedDate'" 
                 type="text" 
                 :value="item.receivedDate"
                 placeholder="yyyy-mm-dd"
                 @input="updateReceivedDate($event,item)"
          >
        </template>
        <template v-slot:[`item.signature`]="{ item }">
            <v-icon v-if="item" @click="openSignatureDialog(item.signature)">
                mdi-text-box-search-outline
            </v-icon>
        </template>
        <template v-slot:[`item.delete`]="{item}">
          <v-icon @click="deleteItem(item)">
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </main>
  </v-card>
</template>

<script>
import * as billApi from "/src/api/billApi"

export default {
  data: () => ({
    headerOption:{
        "sort-icon":null,
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
      { text: "수령일", value: "receivedDate", sortable: false, align: "center" },
      { text: "서명", value: "signature", sortable: false, align: "center" },
      { text:"삭제", value: "delete", sortable:false, align: "center" },
    ],
    totalData:[],
    toDeleteData:[],
    toUpdateData: new Set(),
    signatureDialog:false,
  }),
  created(){
    this.getAllBill();
  },
  computed:{
    //수령날짜 출력 변환
    showReceivedDate: function (val) {
      if (val == null) return "수령 전";
      return val;
    },
  },
  methods: {
    //다이얼로그 닫기 동작
    closeUpdateDialog() {
      this.$emit("closeDialog");
    },
    //임시 데이터(삭제할 데이터, 업데이트할 데이터)를 빈값으로 초기화
    initTempData() {
        this.toDeleteData=[];
        this.toUpdateData= new Set();
    },

    //읽은 엑셀데이터 테이블 비우기
    recoveryAllData() {  
        this.getAllBill();
        this.initTempData();
       
    },
    //수령날짜 출력 변환
    receivedDate: function (val) {
      if (val == null) return "수령 전";
      return val;
    },

    //해당 데이터 행 삭제. 백엔드의 쉬운 처리를 위해 toDeleteData에 idx에 담기
    deleteItem(item){
      const toDeleteItemIndex = this.totalData.indexOf(item)
      this.totalData.splice(toDeleteItemIndex, 1)
      this.toDeleteData.push(item.idx);
    },
    //모든 bill데이터 받아오기
    getAllBill(){
      billApi.getBillAll()
      .then(res=>{
        this.totalData = res.data;
      })
      .catch(err=>{
        console.log(err);
      })
    },
    //서명 확인을 위한 서명 다이얼로그 열기
    openSignatureDialog(){
        this.signatureDialog=true;
    },
    //서명 확인을 위한 서명 다이얼로그 닫기
    closeSignatureDialog(){
        this.signatureDialog=false;
    },
    //서명 확인을 위한 서명 다이얼로그 닫기
    deleteSignatureDialog(){
        this.signatureDialog=null;
    },
    //수정 완료 저장해 둔 임시 삭제 리스트와 테이블에 남은 모든 데이터 패치
    updateDb(){
        const updateDataArr = [... this.toUpdateData];
        billApi.updateBillList(updateDataArr)
        .then(res => {console.log(res)})
        .catch(err => {console.log(err)});

        billApi.deleteBillList(this.toDeleteData)
        .then(res => {console.log(res)})
        .catch(err => {console.log(err)});

        this.getAllBill();
        this.initTempData();
    },
    //연번 데이터 수정 input handler
    updateIdx(event,item){
        item.idx = event.target.value;
        this.toUpdateData.add(item);
    },
    //이름 데이터 수정 input handler
    updateName(event,item){
        item.name = event.target.value;
        this.toUpdateData.add(item);
    },
    //생년월일 데이터 수정 input handler
    updateBirthDate(event,item){
        item.birthDate = event.target.value;
        this.toUpdateData.add(item);
    },
    //거주동 데이터 수정 input handler
    updateLocation(event,item){
        item.location = event.target.value;
        this.toUpdateData.add(item);
    },
    //수량 데이터 수정 input handler
    updateAmount(event,item){
        item.amount = event.target.value;
        this.toUpdateData.add(item);
    },
    //수령일 데이터 수정 input handler
    updateReceivedDate(event,item){
        item.receivedDate = event.target.value;
        this.toUpdateData.add(item);
    },
    addData(){
        this.totalData.unshift({});
    }
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
#table-add-btn{
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

.loaded-table input{
  text-align: center;
}
.loaded-table input[type="text"]{
  width:100%;
  
}
.loaded-table input[type="number"]{
  width:50%;
}
.input-idx{
  width:80% !important;
}
.loaded-table input[type="number"]::-webkit-outer-spin-button,
.loaded-table input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

table.dataTable thead .sorting_asc i{
    display: none !important;
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