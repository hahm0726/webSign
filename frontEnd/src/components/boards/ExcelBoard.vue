<template>
  <v-card>
    <header id="dialog-header">
      <div class="dialog-header-wrap">
        <input
          id="file-input"
          type="file"
          @change="readExcel"
          accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
        />
        <v-spacer></v-spacer>
        <v-btn id="close-btn" icon @click="closeExcelDialog">
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
        :items="excelData"
        hide-default-footer
        :items-per-page="itemsPerPage"
      >
        <template v-slot:top>
          <div class="loaded-table-top">
            <div class="loaded-table-title-area">
              <div class="loaded-table-title table-title-text">
                <span class="title-text">불러온 데이터</span>
                <v-icon class="title-icon" color="rgb(31, 111, 68)">
                  mdi-microsoft-excel
                </v-icon>
              </div>
            </div>
            <div class="btn-group">
              <v-btn
                id="table-clear-btn"
                :disabled="excelData.length <= 0"
                color="error"
                @click="clearTable"
              >
                <span class="btn-text">데이터 초기화</span>
                <v-icon class="icon-in-btn"> mdi-sync </v-icon>
              </v-btn>
              <v-btn
                id="save-to-db-btn"
                :disabled="excelData.length <= 0"
                class="white--text"
                color="rgb(31, 111, 68)"
                @click="saveExcelData"
              >
                <span class="btn-text"> DB 저장</span>
                <v-icon class="icon-in-btn"> mdi-database-plus </v-icon>
              </v-btn>
            </div>
          </div>
        </template>

        <template v-slot:[`item.idx`]="{item}">
          <input :id="item.idx + '_idx'" type="number" v-model="item.idx">
        </template>
        <template v-slot:[`item.name`]="{item}">
          <input :id="item.idx + '_name'" type="text" v-model="item.name">
        </template>
        <template v-slot:[`item.birthDate`]="{item}">
          <input :id="item.idx + 'birthDate'" type="text" v-model="item.birthDate">
        </template>
        <template v-slot:[`item.location`]="{item}">
          <input :id="item.idx + '_location'" type="text" v-model="item.location">
        </template>
        <template v-slot:[`item.amount`]="{item}">
          <input :id="item.idx + '_amount'" type="number" v-model="item.amount">
        </template>
        <template v-slot:[`item.action`]="{item}">
          <v-icon @click="deleteItem(item)">
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </main>
  </v-card>
</template>

<script>
import XLSX from "xlsx";
import * as billApi from "/src/api/billApi"

export default {
  data: () => ({
    noDataText: "아직 불러온 데이터가 없습니다",
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
      {text:"작업", value: "action", sortable:false, align: "center"},
    ],
    itemsPerPage: 10,
    excelData: [],
  }),
  
  methods: {
    //다이얼로그 닫기 동작
    closeExcelDialog() {
      this.$emit("closeDialog");
    },

    //입력된 파일 읽기
    readExcel(event) {
      const file = event.target.files[0]; //입력된 파일
      //파일타입 검사
      if (!this.fileTypeValidate(file)) {
        alert("해당 파일형식을 지원하지 않습니다. ( xls,xlsx,csv 가능)");
        event.target.files = null; //입력된 파일 초기화
        return;
      }
      var reader = new FileReader();
      this.excelData = [];

      const header = ["idx", "name", "birthDate", "location"];
      reader.onload = () => {
        var data = reader.result;
        var wb = XLSX.read(data, {
          type: "binary",
          cellDates: true,
          dateNF: "YYYY-MM-DD",
        });
        wb.SheetNames.forEach((sheetName) => {
          var rows = XLSX.utils.sheet_to_json(wb.Sheets[sheetName], {
            header: header,
            range: 1,

            raw: false,
          });
          for (var i = 0; i < rows.length; i++) {
            rows[i].amount=0;
            this.excelData.push(rows[i]);
          }
        });
      };
      reader.readAsBinaryString(file);

    },

    //파일타입 검사
    fileTypeValidate(file) {
      const filetype = file.name.split(".")[1];
      if (filetype === "xls" || filetype === "xlsx" || filetype === "csv") {
        return true;
      }
      return false;
    },
    //읽은 엑셀데이터 테이블 비우기
    clearTable() {
      const fileinput = document.querySelector('#file-input');
      fileinput.files = null;
      fileinput.value = null;
      this.excelData = [];
    },

    //읽은 엑셀 데이터 DB에 저장
    saveExcelData(){
      billApi.createBillList(this.excelData)
      .then(()=>{
        this.$emit("excelDataSaved");
      })
      .catch(err=>{
        console.log(err);
      })
    },
    //해당 데이터 행 삭제
    deleteItem(item){
      const toDeleteItemIndex = this.excelData.indexOf(item)
      this.excelData.splice(toDeleteItemIndex, 1)
      if(this.excelData.length == 0){
        this.clearTable();
      }
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
  border-bottom: 3px solid rgb(31, 111, 68);
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

.loaded-table input[type="number"]::-webkit-outer-spin-button,
.loaded-table input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
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