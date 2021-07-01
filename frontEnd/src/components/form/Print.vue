<template>
  <div class="a4 print-area">
    <table id="print-form">
      <thead>
        <tr>
          <th colspan="6">{{formTitle}}</th>
        </tr>
        <tr>
          <th colspan="2">후원처</th>
          <th colspan="2">독거노인종합지원센터</th>
          <th>품목</th>
          <th>효 박스</th>
        </tr>
        <tr>
          <th>연번</th>
          <th>수령일</th>
          <th>성명</th>
          <th>생년월일</th>
          <th>수량</th>
          <th>수령확인(개인)</th>
        </tr>
      </thead>
      <tbody>
        <!-- 단일 반복문 이용한 출력 -->
        <tr v-for="i in 10" :key="i">
          <td v-if="i <= printDataLen">
            {{ printData[i - 1].idx }}
          </td>
          <td v-else></td>
          <td v-if="i <= printDataLen">
            {{ printData[i - 1].receivedDate }}
          </td>
          <td v-else></td>
          <td v-if="i <= printDataLen">{{ printData[i - 1].name }}</td>
          <td v-else></td>
          <td v-if="i <= printDataLen">{{ printData[i - 1].birthDate }}</td>
          <td v-else></td>
          <td v-if="i <= printDataLen">{{ printData[i - 1].amount }}</td>
          <td v-else></td>
          <td v-if="i <= printDataLen">
            <img v-if="printData[i - 1].signature !== null" class="sign-img" :src="printData[i - 1].signature">
          </td>
          <td v-else></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    formTitle:String,
    printData:Array
  },
  computed: {
    printDataLen() {
      if(this.printData == undefined) return 0;
      return this.printData.length;
    },
  }
};
</script>

<style scoped>
/* 테이블 전체 디자인 */
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
}
</style>
