<template>
  <div>
    <v-btn @click="print">인쇄</v-btn>
    <v-data-table
      mobile-breakpoint="0"
      class="tables"
      :headers="thItems"
      :items="tdItems"
      :items-per-page="itemsPerPage"
      hide-default-footer
    >
      <template v-slot:top>
        <v-dialog v-model="dialog" persistent max-width="500px">
          <v-card class="pa-2">
            <vue-signaturePad
              class="canvas-color"
              width="100%"
              height="200px"
              ref="signaturePad"
              :options="{
                onBegin: () => {
                  $refs.signaturePad.resizeCanvas();
                },
              }"
            >
            </vue-signaturePad>

            <v-btn class="mt-2" small @click="clearCanvas">지우기</v-btn>

            <v-card-actions class="pa-0">
              <v-spacer></v-spacer>
              <v-btn color="error white--text" small @click="closeDialog">
                취소
              </v-btn>
              <v-btn
                color="blue darken-1 white--text"
                small
                @click="closeDialog"
              >
                서명완료
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>

      <template v-slot:[`item.receivedDate`]="{ item }">
        {{ receivedDate(item.receivedDate) }}
      </template>
      <template v-slot:[`item.state`]="{ item }">
        {{ isReceived(item.state) }}
      </template>
      <template v-slot:[`item.action`]="{ item }">
        <v-icon v-if="item.state" @click="openDialog(item)">
          mdi-text-box-search-outline
        </v-icon>
        <v-icon v-else :disabled="item.state" @click="openDialog(item)">
          mdi-draw
        </v-icon>
      </template>
      <template v-slot:footer>
        <v-pagination
          v-model="page"
          :length="pageCount"
          :total-visible="totalVisible"
          next-icon="mdi-menu-right"
          prev-icon="mdi-menu-left"
        ></v-pagination>
      </template>
    </v-data-table>
    <!-- 프린트 영역 페이지에 안보이도록 출력 -->
    <print v-bind:print_data="this.tdItems" class="print-visible"></print>
  </div>
</template>

<script>
import { Printd } from "printd";
import Print from "@/components/form/Print";

export default {
  components: { Print },
  data: () => ({
    dialog: false, //다이얼로그 상태값
    itemsPerPage: 10, // 테이블 페이지당 보여지는 아이템 수
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
    tdItems: [
      {
        idx: 1,
        name: "홍길동",
        birthDate: "1999-07-26",
        location: "안양2동",
        amount: 1,
        receivedDate: null,
        state: true,
      },
      {
        idx: 2,
        name: "홍길동",
        birthDate: "1999-07-26",
        location: "안양2동",
        amount: 1,
        receivedDate: null,
        state: true,
      },
      {
        idx: 3,
        name: "홍길동",
        birthDate: "1999-07-26",
        location: "안양2동",
        amount: 1,
        receivedDate: null,
        state: true,
      },
      {
        idx: 4,
        name: "길동홍",
        birthDate: "1999-07-26",
        location: "안양2동",
        amount: 1,
        receivedDate: null,
        state: true,
      },
      {
        idx: 5,
        name: "홍길동",
        birthDate: "1999-07-26",
        location: "안양2동",
        amount: 1,
        receivedDate: null,
        state: true,
      },
      {
        idx: 6,
        name: "김상만",
        birthDate: "1993-08-21",
        location: "안양1동",
        amount: 2,
        receivedDate: null,
        state: false,
      },
      {
        idx: 7,
        name: "최길자",
        birthDate: "1923-03-26",
        location: "안양1동",
        amount: 1,
        receivedDate: null,
        state: false,
      },
    ],
  }),

  methods: {
    // 수령 상태 출력 변환
    isReceived: function(val) {
      if (val === true) return "수령완료";
      return "수령 전";
    },
    //수령날짜 출력 변환
    receivedDate: function(val) {
      if (val === null) return "수령 전";
      return val;
    },
    //다이얼로그 열기
    openDialog() {
      this.dialog = true;
    },
    //다이얼로그 닫기
    closeDialog() {
      this.dialog = false;
      this.clearCanvas();
    },

    clearCanvas() {
      this.$refs.signaturePad.clearSignature();
    },
    save() {
      const { isEmpty, data } = this.$refs.signaturePad.saveSignature();
      console.log(isEmpty);
      console.log(data);
    },
    print() {
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
.canvas-color {
  background-color: lightgray;
  border: 1px solid black;
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
