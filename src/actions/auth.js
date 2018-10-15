import {
  LOGIN_USER,
  LOGOUT_USER
} from '../constants/index'


export function loginUser(email) {
  return {
    type: LOGIN_USER,
    user: email
  };
}

export function logoutUser() {
  return {
    type: LOGOUT_USER
  };
}
