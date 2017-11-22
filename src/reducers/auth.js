import {
  LOGIN_USER,
  LOGOUT_USER,
} from "../constants/index"


const defaultState = {
  authenticated: false,
};


export function auth(state = defaultState, action) {
  switch (action.type) {
    case LOGIN_USER:
      return {...state, authenticated: true};
    case LOGOUT_USER:
      return {...state, authenticated: false};
    default:
      return state;
  }
}