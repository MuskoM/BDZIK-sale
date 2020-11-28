import axios from 'axios';
import {createMessage, returnErrors} from './messages'

import {GET_COMPUTER_LABS, DELETE_COMPUTER_LAB, ADD_COMPUTER_LAB} from './types'

//Get computer_labs
export const getComputerLabs = () => (dispatch, getState) => {
    axios.get('/api/pracownie_specjalistyczne/', tokenConfig(getState)).then((res) => {
        dispatch({
            type: GET_COMPUTER_LABS,
            payload: res.data,
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};

//Delete computer_lab
export const deleteComputerLab = (id) => (dispatch, getState) => {
    axios.delete('/api/pracownie_specjalistyczne/${id}', tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ deleteComputerLab: 'ComputerLab deleted'}));
        dispatch({
            type: DELETE_COMPUTER_LAB,
            payload: id,
        });
    }).catch((err) => console.log(err));
};

//Add computer_lab
export const addComputerLab = (computer_lab) => (dispatch, getState) => {
    axios.post('/api/pracownie_specjalistyczne/', computer_lab, tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ addComputerLab: 'Added new computer_lab' }));
        dispatch({
            type: ADD_COMPUTER_LAB,
            payload: res.data
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};