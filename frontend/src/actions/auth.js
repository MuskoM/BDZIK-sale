import axios from 'axios';
import { returnErrors } from './messages'

import {
    USER_LOADED,
    USER_LOADING,
    AUTH_ERROR,
    LOGIN_FAIL,
    LOGIN_SUCCESS,
    LOGOUT_SUCCESS,
    REGISTER_SUCCESS,
    REGISTER_FAIL
} from "./types";

//check token & load particular user
export const loadUser = () => (dispatch, getState) => {
    dispatch({ type: USER_LOADING });

    axios.get('/api/auth/user', tokenConfig(getState)).then((res) => {
        dispatch({
            type: USER_LOADED,
            payload: res.data
        });
    }).catch((err) => {
        dispatch(returnErrors(err.response.data, err.response.status));
        dispatch({
            type: AUTH_ERROR});
    });
};

//login user
export const loginUser = (username, password) => (dispatch) => {
    const config = {
        headers: {
            'Content-Type' : 'application/json',
        },
    };

    const body = JSON.stringify({username, password });

    axios.post('/api/auth/login', body, config).then((res) => {
        dispatch({
            type: LOGIN_SUCCESS,
            payload: res.data});
    }).catch((err) => {
        dispatch(returnErrors(err.response.data, err.response.status));
        dispatch({
            type: LOGIN_FAIL});
    });
};

//Logout the user
export const logoutUser = () => (dispatch, getState) => {
  axios
    .post('/api/auth', null, tokenConfig(getState))
    .then((res) => {
      dispatch({ type: 'CLEAR_LEADS' });
      dispatch({
        type: LOGOUT_SUCCESS,
      });
    })
    .catch((err) => {
      dispatch(returnErrors(err.response.data, err.response.status));
    });
};

// Setup config with token - helper function
export const tokenConfig = (getState) => {
  // Get token from state
  const token = getState().auth.token;

  // Headers
  const config = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // If token, add to headers config
  if (token) {
    config.headers['Authorization'] = `Token ${token}`;
  }

  return config;
};

//Register new user
export const registerUser = ({ username, password, email }) => (dispatch) => {
  const config = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const body = JSON.stringify({ username, email, password });

  axios.post('/api/auth/register', body, config).then((res) => {
      dispatch({
        type: REGISTER_SUCCESS,
        payload: res.data,
      });
    }).catch((err) => {
      dispatch(returnErrors(err.response.data, err.response.status));
      dispatch({
        type: REGISTER_FAIL,
      });
    });
};