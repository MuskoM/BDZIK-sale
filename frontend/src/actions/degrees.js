import axios from 'axios';
import {createMessage, returnErrors} from './messages'

import {GET_DEGREES, DELETE_DEGREE, ADD_DEGREE} from './types'

//Get Degrees
export const getDegrees = () => (dispatch, getState) => {
    axios.get('/api/kierunki/', tokenConfig(getState)).then((res) => {
        dispatch({
            type: GET_DEGREES,
            payload: res.data,
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};

//Delete reservation
export const deleteDegree = (id) => (dispatch, getState) => {
    axios.delete('/api/kierunki/${id}', tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ deleteDegree: 'Degree deleted'}));
        dispatch({
            type: DELETE_DEGREE,
            payload: id,
        });
    }).catch((err) => console.log(err));
};

//Add reservation
export const addDegree = (Degree) => (dispatch, getState) => {
    axios.post('/api/kierunki/', Degree, tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ addDegree: 'Added new Degree' }));
        dispatch({
            type: ADD_DEGREE,
            payload: res.data
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};