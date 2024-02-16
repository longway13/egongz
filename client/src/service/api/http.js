import axios from 'axios';

let url = 'http://localhost:8000/';
//섹션 로그인 기능
export function get(link) {
  return axios.get(url + link);
}

export function getWithParam(link, param) {
  return axios.get(url + link, { params: param });
}

export function post(link, data) {
  return axios.post(url + link, data);
}

export function getWithTokenNParam(link, param, token) {
  return axios.get(url + link, {
    params: param,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function postWithToken(link, data, token) {
  return axios.post(url + link, data, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function getWithToken(link, token) {
  return axios.get(url + link, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function deleteWithToken(link, id, token) {
  return axios.delete(url + link + id, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
