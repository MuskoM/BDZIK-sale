import axios from 'axios';
import {createMessage, returnErrors} from './messages'

import {GET_STUDENTS, DELETE_STUDENT, ADD_STUDENT} from './types'

//Get students
export const getStudents = () => (dispatch, getState) => {
    axios.get('/api/wydzialy/', tokenConfig(getState)).then((res) => {
        dispatch({
            type: GET_STUDENTS,
            payload: res.data,
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};

//Delete student
export const deleteStudent = (id) => (dispatch, getState) => {
    axios.delete('/api/wydzialy/${id}/', tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ deleteStudent: 'Student deleted'}));
        dispatch({
            type: DELETE_STUDENT,
            payload: id,
        });
    }).catch((err) => console.log(err));
};

//Add student
export const addStudent = (student) => (dispatch, getState) => {
    axios.post('/api/wydzialy/', student, tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ addStudent: 'Added new student' }));
        dispatch({
            type: ADD_STUDENT,
            payload: res.data
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};