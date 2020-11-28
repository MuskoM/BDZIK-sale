import axios from 'axios';
import {createMessage, returnErrors} from './messages'

import {GET_ROOMS, DELETE_ROOM, ADD_ROOM} from './types'

//Get rooms
export const getRooms = () => (dispatch, getState) => {
    axios.get('/api/sale/', tokenConfig(getState)).then((res) => {
        dispatch({
            type: GET_ROOMS,
            payload: res.data,
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};

//Delete room
export const deleteRoom = (id) => (dispatch, getState) => {
    axios.delete('/api/sale/${id}', tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ deleteRoom: 'Room deleted'}));
        dispatch({
            type: DELETE_ROOM,
            payload: id,
        });
    }).catch((err) => console.log(err));
};

//Add room
export const addRoom = (room) => (dispatch, getState) => {
    axios.post('/api/sale/', room, tokenConfig(getState)).then((res) => {
        dispatch(createMessage({ addRoom: 'Added new room' }));
        dispatch({
            type: ADD_ROOM,
            payload: res.data
        });
    }).catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
};