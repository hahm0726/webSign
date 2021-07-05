<template>
 <v-app>
  <v-main >
    <v-container fill-height fluid class="my-auto d-flex align-center">
      <!--전체 화면 정렬을 위한 row-->
      <v-row justify="center">
        <v-col>
          <!--로그인 카드 영역-->
          <v-card class="mx-auto" max-width="374" elevation="0">
            <!--로그인 카드 이미지 영역-->
            <v-img
              max-height="250"
              :src="require(`/src/assets/logo.png`)"
            ></v-img>
            <!--로그인 카드 인풋 영역-->
            <v-container fill-height>
              <v-row class="mx-auto">
                <!--아이디/비밀번호 col 영역 비율 8 차지-->
                <v-col cols="8">
                  <v-text-field
                    v-model="data.username"
                    hide-details="auto"
                    outlined
                    fiiled
                    class="mb-2"
                    elevation="2"
                    placeholder="아이디"
                  ></v-text-field>
                  <v-text-field
                    v-model="data.password"
                    hide-details="auto"
                    outlined
                    type="password"
                    elevation="2"
                    placeholder="비밀번호"
                  ></v-text-field>
                </v-col>
                <!-- 로그인 버튼 col 영역 비율 4 차지-->
                <v-col cols="4">
                  <v-btn id="login-btn" width="100%" height="100%" @click="login()">
                    로그인
                  </v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</v-app>
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

<style scoped>
#login-btn{
  background-color: white;
  border: 1px solid;
  text-align: center;
}
</style>
