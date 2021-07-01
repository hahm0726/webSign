<template>
  <v-data-table
    v-model="toPrintItems"
    mobile-breakpoint="0"
    class="tables loaded-table"
    :headers="thItems"
    :items="tdItems"
    show-select
    item-key="idx"
  >
    <template v-slot:top>
      <v-dialog v-model="dialog" persistent max-width="500px">
        <component :is="selectedDialog" @closeDialog="closeDialog" @reRender="getAllBill" :item="selectedItem"></component>
      </v-dialog>
      <print :formTitle="formTitle" :printData="toPrintItems" class="print-visible"></print>
      <div class="loaded-table-top">
        <div class="loaded-table-title-area">
          <div class="loaded-table-title table-title-text">
            <span class="title-input" role="textbox" @input="onTitleInput($event)" contenteditable>{{formTitle}}</span>
            <v-icon class="title-icon" color="black">
                  mdi-file-document-outline
            </v-icon>
          </div>
        </div>
        <v-btn @click="print">인쇄</v-btn>
      </div>
    </template>
    <template v-slot:[`item.receivedDate`]="{ item }">
      {{ receivedDate(item.receivedDate) }}
    </template>
    <template v-slot:[`item.state`]="{ item }">
      {{ isReceived(item.signature) }}
    </template>
    <template v-slot:[`item.action`]="{ item }">
      <v-icon v-if="item.signature == null || item.signature== undefined"
              @click="openSignDialog(item)"
      >
        mdi-draw
      </v-icon>
      <v-icon v-else @click="openImgDialog(item)">
        mdi-text-box-search-outline
      </v-icon>   
    </template>
  </v-data-table>
</template>

<script>
import { Printd } from "printd";
import Print from "@/components/form/Print";
import SignDialog from "/src/components/dialog/SignDialog"
import ImgDialog from "/src/components/dialog/ImgDialog"
import * as billApi from "/src/api/billApi"


export default {
  components: { 
    Print,
    SignDialog,
    ImgDialog,
  },
  data: () => ({

    formTitle:"인수증",
    dialog:false,
    signDialog:false,
    imgDialog:false,
    selectedDialog:null,
    selectedItem: {},
    toPrintItems:[],
    thItems: [
      { text: "연번", value: "idx", sortable: false, align: "center" },
      { text: "이름", value: "name", sortable: false, align: "center" },
      {
        text: "생년월일",
        value: "birthDate",
        sortable: false,
        align: "center",
      },
      { text: "거주동", value: "location", sortable: false, align: "center" },
      { text: "수량", value: "amount", sortable: false, align: "center" },
      {
        text: "수령일",
        value: "receivedDate",
        sortable: false,
        align: "center",
      },
      { text: "수령상태", value: "state", sortable: false, align: "center" },
      { text: "작업", value: "action", sortable: false, align: "center" },
    ],
    tdItems: [],
  }),
  created(){
    this.getAllBill();
  },
  methods: {
    // 수령 상태 출력 변환
    isReceived: function (val) {
      if (val == null || val== undefined) return "수령 전";
      return "수령완료";
    },
    //수령날짜 출력 변환
    receivedDate: function (val) {
      if (val == null) return "수령 전";
      return val;
    },
    //사인 다이얼로그 열기
    openSignDialog(item) {
      this.selectedItem= item;
      this.selectedDialog=SignDialog;
      this.signDialog = true;
      this.dialog = this.signDialog;
    },
    
    //사인확인 다이얼로그 열기
    openImgDialog(item) {
      this.selectedItem= item;
      this.selectedDialog=ImgDialog;
      this.signDialog = true;
      this.dialog = this.signDialog;
    },
     //사인 다이얼로그 닫기
    closeSignDialog() {
      this.signDialog = false;
      this.selectedDialog=null;
      this.dialog = this.signDialog;
    },
    //사인확인 다이얼로그 닫기
    closeImgDialog() {
      this.imgDialog = false;
      this.selectedDialog=null;
      this.dialog = this.imgDialog;
    },

    //열린 다이얼로그에 따라 다이얼로그 닫기 함수 선택 제공
    closeDialog() {
      this.selectedItem= {};
      if(this.signDialog) return this.closeSignDialog();
      if(this.imgDialog) return this.closeImgDialog();
    },
    
    //모든 bill데이터 받아오기
    getAllBill(){
      billApi.getBillAll()
      .then(res=>{
        this.tdItems = res.data;
      })
      .catch(err=>{
        console.log(err);
      })
    },
    onTitleInput: function(e) {
      this.formTitle = e.target.innerHTML;
    },
    print() {
      console.log(this.toPrintItems);
      const d = new Printd();
      const css = `/* 테이블 전체 디자인 */
                    #print-form {
                      width: 100%;
                      height: 100%;
                      text-align: center;
                      font-size: 15pt;
                    }
                    /* 헤드 첫줄 제목 디자인 */
                    #print-form thead > tr:nth-child(1) {
                      font-size: 25pt;
                    }
                    /* 테이블 헤드의 th 디자인 */
                    #print-form thead th {
                      padding-top: 10px;
                      padding-bottom: 10px;
                    }

                    /* 테이블 바디 여백 */
                    #print-form tbody td {
                      height: 80px;
                    }

                    /* 테이블 테두리 한줄 설정 */
                    #print-form,
                    td,
                    th {
                      border: 1px solid black;
                      border-collapse: collapse;
                    }

                    .sign-img{
                      width:90px;
                      height:50px;
                    }
                    /* A4 사이즈 설정 */
                    @page a4sheet {
                      size: 21cm 29.7cm;
                    }
                    .a4 {
                      page: a4sheet;
                      page-break-after: always;
                    }

                    .print-area {
                      display: flex;
                      align-items: center;
                    }`;

      const print_sheet = document.querySelector(".print-area");
      d.print(print_sheet, [css]);
    },
  },
};
</script>

<style scoped>
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
  width:fit-content;
  font-size: 24px;
  font-weight: bold;
}
.title-input{
  min-width: 10px;
}
.title-icon {
  padding-left: 15px;
  padding-right: 15px;
}

.print-visible {
  display: none;
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

@media print {
  .print-visible {
    display: initial;
  }
}
</style>