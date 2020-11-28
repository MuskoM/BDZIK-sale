import axios from 'axios';
import {createMessage, returnErrors} from './messages'

import {GET_LABS, DELETE_LAB, ADD_LAB} from './types'

//Get labs
export const getLabs = () => (dispatch, getState) => {
    axios.get('/api/laboratoria/', tokenConfig(getState)).then((res) => {
        dispatch({
            type: GET_LABS,
            payload: res.data,
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};

//Delete lab
export const deleteLab = (id) => (dispatch, getState) => {
    axios.delete('/api/laboratoria/${id}', tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ deleteLab: 'Lab deleted'}));
        dispatch({
            type: DELETE_LAB,
            payload: id,
        });
    }).catch((err) => console.log(err));
};

//Add lab
export const addLab = (lab) => (dispatch, getState) => {
    axios.post('/api/laboratoria/', lab, tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ addLab: 'Added new lab' }));
        dispatch({
            type: ADD_LAB,
            payload: res.data
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};