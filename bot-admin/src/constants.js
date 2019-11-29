const WEBSOCKET_PATH = '/discussion';
const SERVER_URL = (process.env.NODE_ENV === 'development'?'localhost:8888':null);
export default {
    SERVER_URL: `http://${SERVER_URL}`,
    WEBSOCKET_URL: `ws://${SERVER_URL}${WEBSOCKET_PATH}`,
};
