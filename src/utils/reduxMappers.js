import {
  loginUser,
  logoutUser,
} from '../actions/auth'

export const mapStateToProps = (state) => {
  return {
    authenticated: state.authenticated,
    user: state.user
  }
};

export const mapDispatchToProps = (dispatch) => {
  return {
    login: (email) => {
      dispatch(loginUser(email))
    },
    logout: () => {
      dispatch(logoutUser())
    }
  }
};
