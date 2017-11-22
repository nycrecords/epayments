import {
  loginUser,
  logoutUser,
} from '../actions/auth'

export const mapStateToProps = (state) => {
  return {
    authenticatedFE: state.authenticated
  }
};

export const mapDispatchToProps = (dispatch) => {
  return {
    loginFE: () => {
      dispatch(loginUser())
    },
    logoutFE: () => {
      dispatch(logoutUser())
    },
    register: () => {
      dispatch(registerUser())
    },
    deregister: () => {
      dispatch(deregisterUser())
    },
    approve: () => {
      dispatch(approveUser())
    },
    deny: () => {
      dispatch(denyUser())
    }
  }
};
