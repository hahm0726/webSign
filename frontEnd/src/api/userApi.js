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

function deleteUser(userId) {
  const url = `/users/api/user/${userId}/`;
  return axiosService.delete(url);
}

function updateUser(userId, data) {
  const url = `/users/api/user/${userId}/`;
  return axiosService.patch(url, data);
}

export {
  getUsers,
  createUser,
  deleteUser,
  updateUser,
};
