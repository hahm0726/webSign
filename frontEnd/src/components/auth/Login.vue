<template>
  <!--전체 화면 정렬을 위한 row-->
  <v-row justify="center">
    <v-col>
      <!--로그인 카드 영역-->
      <v-card class="mx-auto" max-width="374">
        <!--로그인 카드 이미지 영역-->
        <v-img
          max-height="250"
          src="https://picsum.photos/id/11/500/300"
        ></v-img>
        <!--로그인 카드 인풋 영역-->
        <v-container fill-height>
          <v-row class="mx-auto mt-2">
            <!--아이디/비밀번호 col 영역 비율 8 차지-->
            <v-col cols="8">
              <v-text-field
                v-model="data.username"
                hide-details="auto"
                placeholder="아이디"
              ></v-text-field>
              <v-text-field
                v-model="data.password"
                hide-details="auto"
                type="password"
                placeholder="패스워드"
              ></v-text-field>
            </v-col>
            <!-- 로그인 버튼 col 영역 비율 4 차지-->
            <v-col cols="4">
              <v-btn width="100%" height="100%" @click="login()">
                로그인
              </v-btn>
            </v-col>
          </v-row>
          <!-- 아이디 / 비밀번호 찾기, 회원가입 버튼-->
          <v-row justify="center">
            <v-col>
              <v-btn text @click="moveToFindID()">아이디 찾기</v-btn>
              <v-btn text @click="moveToFindPW()">비밀번호 찾기</v-btn>
              <v-btn text @click="moveToSignup()">회원가입</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import axios from "axios";

export default {
  data: () => {
    return {
      data: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    // router 이용하여 이동할 페이지 선언
    moveToSignup: function() {
      var router = this.$router;
      return router.push({ name: "Signup" });
    },
    moveToFindID: function() {
      var router = this.$router;
      return router.push({ name: "FindID" });
    },
    moveToFindPW: function() {
      var router = this.$router;
      return router.push({ name: "FindPW" });
    },
    moveToHome: function() {
      var router = this.$router;
      return router.push({ name: "Home" });
    },
    // 폼에 있는 데이터 삭제하는 함수
    clearPW: function() {
      this.data.password = "";
    },
    // 로그인 함수 정의
    login() {
      axios
        .post("http://127.0.0.1:8000/users/login/", this.data)
        .then((res) => {
          // 요청 성공시 실행
          console.log(res);
          this.moveToHome();
        })
        .catch((err) => {
          // 요청 실패시 실행
          console.log(err.response);
          alert(err.response.data.msg);
          this.clearPW(); // 기존에 입력되어 있던 데이터 삭제
        });
    },
  },
};
</script>

<style></style>
