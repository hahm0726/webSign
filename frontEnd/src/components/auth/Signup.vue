<template>
  <v-row justify="center">
    <v-col cols="8">
      <v-card elevation="2">
        <v-card-title class="text-h4">회원가입</v-card-title>
        <v-card-subtitle>webSign 회원가입</v-card-subtitle>
        <v-divider class="mx-7"></v-divider>

        <div class="mx-7">
          <v-card-text class="font-weight-medium text-h6 pb-0">
            가입정보입력
          </v-card-text>
          <v-row justify="start">
            <v-col cols="6">
              <v-text-field
                v-model="regData.username"
                :error-messages="id_err_msg"
                label="아이디"
                hide-details="auto"
              >
              </v-text-field>
            </v-col>

            <v-col>
              <v-btn large @click="valid_id">중복확인</v-btn>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="6">
              <v-text-field
                label="비밀번호(4자리 이상)"
                v-model="regData.password"
                type="password"
                :error-messages="pw_err_msg"
                hide-details="auto"
              ></v-text-field>
            </v-col>

            <v-col cols="6">
              <v-text-field
                label="비밀번호 확인"
                v-model="regData.password_valid"
                type="password"
                :error-messages="pw_err_msg"
                hide-details="auto"
              ></v-text-field>
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <v-text-field
                v-model="regData.name"
                label="이름"
                hide-details="auto"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                label="회사"
                v-model="regData.company"
                hide-details="auto"
              ></v-text-field>
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <v-text-field
                v-model="regData.department"
                label="부서"
                hide-details="auto"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                label="유저타입"
                v-model="regData.userType"
                hide-details="auto"
              ></v-text-field>
            </v-col>
          </v-row>

          <v-row class="mt-10">
            <v-col>
              <v-btn block large class="mb-7" @click="back">
                이전으로
              </v-btn>
            </v-col>

            <v-col>
              <v-btn block large class="mb-7" @click="next">
                다음으로
              </v-btn>
            </v-col>
          </v-row>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    regData: {
      username: "",
      password: "",
      password_valid: "",
      name: "",
      department: "",
      userType: "",
    },
    id_valid_flag: false, // 아이디 중복확인 여부
  }),
  watch: {
    // 아이디 바꾸면 아이디 검증 플래그 초기화
    "regData.username": function() {
      this.id_valid_flag = false;
    },
  },
  methods: {
    valid_id() {},
  },
};
</script>
