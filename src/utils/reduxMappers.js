import {
  loginUser,
  logoutUser,
} from '../actions/auth'

export const mapStateToProps = (state) => {
  return {
    authenticated: state.authenticated
  }
};

export const mapDispatchToProps = (dispatch) => {
  return {
    login: () => {
      dispatch(loginUser())
    },
    logout: () => {
      dispatch(logoutUser())
    }
  }
};
