import axios from 'axios';

export const axiosService= axios.create({
    baseURL: 'http://127.0.0.1:8000/', // 백엔드 서버 기본 URL
    withCredentials: true,
});

