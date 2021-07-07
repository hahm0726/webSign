import axios from "axios";
import store from "../vuex/config";

export const axiosService = axios.create({
  baseURL: "http://127.0.0.1:8000/", // 백엔드 서버 기본 URL
  headers: {
    Authorization: "JWT " + store.state.userStore.access_token,
    "Content-Type": "application/json",
    accept: "application/json",
  },
  withCredentials: true,
});

/*
  1. 요청 인터셉터
  2개의 콜백 함수를 받습니다.
*/
axiosService.interceptors.request.use(
  // 요청 성공 직전 호출됩니다.
  // axios 설정값을 넣습니다. (사용자 정의 설정도 추가 가능)
  function(config) {
    config.headers.Authorization = "JWT " + store.state.userStore.access_token;
    return config;
  },
  // 요청 에러 직전 호출됩니다.
  function(error) {
    return Promise.reject(error);
  }
);

/*
    2. 응답 인터셉터
    2개의 콜백 함수를 받습니다.
  */
axiosService.interceptors.response.use(
  /*
      http status가 200인 경우
      응답 성공 직전 호출됩니다. 
      .then() 으로 이어집니다.
    */
  function(response) {
    return response;
  },

  /*
      http status가 200이 아닌 경우
      응답 에러 직전 호출됩니다.
      .catch() 으로 이어집니다.    
    */
  function(error) {
    // 에러에서 정보 추출
    const {
      config, // 실패한 기존 요청
      response: { status },
    } = error;

    if (status === 401 && error.response.data.code === "token_not_valid") {
      console.log("액세스 토큰 만료");
      const originalRequest = config;
      const refreshToken = store.state.userStore.refresh_token;
      // 리프레시 토큰 이용하여 새로운 액세스 토큰 요청
      console.log("새로운 토큰 요청");

      try {
        const res = axiosService.post("/users/refresh/", {
          refresh: refreshToken,
        });
        console.log("액세스 토큰 재발급 성공");
        // 세션 저장소의 액세스 토큰 업데이트
        store.commit("setAccess", res.data.access);
        // 원래 요청의 헤더에 있는 토큰 새로 발급받은 토큰으로 변경
        originalRequest.headers.Authorization =
          "JWT " + store.state.userStore.access_token;
        // 실패했던 기존 요청 새로운 토큰 이용하여 다시 실행
        return axios(originalRequest);
      } catch (err) {
        console.log("액세스 토큰 재발급 실패(리프레시 토큰 만료)");
        console.log(err.response);
        sessionStorage.clear(); // 세션 저장소의 데이터 삭제
        alert("세션이 만료되었습니다 다시 로그인 해주세요.");
        window.location.href = "http://127.0.0.1:8080/";
      }
    }
    return Promise.reject(error);
  }
);

export default axiosService;
