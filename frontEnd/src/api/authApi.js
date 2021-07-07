import { axiosService } from "/src/api/config";

/* 유저 로그인 요청 */
function login(data) {
  const url = "/users/login/";
  return axiosService.post(url,data);
}

export {
  login,
};
