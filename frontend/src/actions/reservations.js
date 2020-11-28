import axios from 'axios';
import {createMessage, returnErrors} from './messages'

import {GET_RESERVATIONS, DELETE_RESERVATION, ADD_RESERVATION} from './types'

//Get reservation
export const getReservations = () => (dispatch, getState) => {
    axios.get('/api/rezerwacje_sal/', tokenConfig(getState)).then((res) => {
        dispatch({
            type: GET_RESERVATIONS,
            payload: res.data,
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};

//Delete reservation
export const deleteReservation = (id) => (dispatch, getState) => {
    axios.delete('/api/rezerwacje_sal/${id}', tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ deleteReservation: 'Reservation deleted'}));
        dispatch({
            type: DELETE_RESERVATION,
            payload: id,
        });
    }).catch((err) => console.log(err));
};

//Add reservation
export const addReservation = (reservation) => (dispatch, getState) => {
    axios.post('/api/rezerwacje_sal/', reservation, tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ addReservation: 'Added new reservation' }));
        dispatch({
            type: ADD_RESERVATION,
            payload: res.data
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};