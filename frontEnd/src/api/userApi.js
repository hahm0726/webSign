import { axiosService } from "/src/api/config";

/* 유저 리스트 요청 */
function getUsers() {
  const url = "/users/api/user/";
  return axiosService.get(url);
}

/* 유저 생성 요청 */
function createUser(data) {
  const url = "/users/api/user/";
  return axiosService.post(url, data);
}

/* 유저 삭제 요청 */
function deleteUser(userId) {
  const url = `/users/api/user/${userId}/`;
  return axiosService.delete(url);
}

/* 유저 수정 요청 */
function updateUser(userId, data) {
  const url = `/users/api/user/${userId}/`;
  return axiosService.patch(url, data);
}

/* 아이디 중복 확인 요청 */
async function isUserNameDuplicated(username) {
  const url = `users/api/user/chk_username/?username=${username}`;
  return await axiosService.get(url);
}

export {
  getUsers,
  createUser,
  deleteUser,
  updateUser,
  isUserNameDuplicated,
};
