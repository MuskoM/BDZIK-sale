import axios from 'axios';
import {createMessage, returnErrors} from './messages'

import {GET_DEPARTMENTS, DELETE_DEPARTMENT, ADD_DEPARTMENT} from './types'

//Get departments
export const getDepartments = () => (dispatch, getState) => {
    axios.get('/api/wydzialy/', tokenConfig(getState)).then((res) => {
        dispatch({
            type: GET_DEPARTMENTS,
            payload: res.data,
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};

//Delete reservation
export const deleteDepartment = (id) => (dispatch, getState) => {
    axios.delete('/api/wydzialy/${id}', tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ deleteDepartment: 'Department deleted'}));
        dispatch({
            type: DELETE_DEPARTMENT,
            payload: id,
        });
    }).catch((err) => console.log(err));
};

//Add reservation
export const addDepartment = (department) => (dispatch, getState) => {
    axios.post('/api/wydzialy/', department, tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ addDepartment: 'Added new department' }));
        dispatch({
            type: ADD_DEPARTMENT,
            payload: res.data
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};