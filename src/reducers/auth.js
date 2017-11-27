import {
  LOGIN_USER,
  LOGOUT_USER,
} from "../constants/index"


const defaultState = {
  authenticated: false,
  user: ''
};


export function auth(state = defaultState, action) {
  switch (action.type) {
      case LOGIN_USER:
      return {...state, authenticated: true, user: action.user};
    case LOGOUT_USER:
      return {...state, authenticated: false, user: ''};
    default:
      return state;
  }
}