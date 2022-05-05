class Socket {
    static SOCKET_DEFAULT_LINK = "http://localhost:3000";
    static SOCKET_LINK = Socket.SOCKET_DEFAULT_LINK;
    static instance;
    static setups = [];
    static timeoutID = -1;

    static attachSetup(callback) {
        Socket.setups.push(callback);
        callback(Socket.getInstance());
    }

    static getInstance() {
        if (Socket.instance == null) {
            Socket.instance = io(Socket.SOCKET_LINK);
            Socket.setups.forEach(setup => setup(Socket.instance));
        }
        return Socket.instance;
    }

    static setLink(link) {
        Socket.SOCKET_LINK = link;
        if (Socket.instance != null) Socket.instance.close();
        Socket.instance = null;

        if (Socket.timeoutID != -1) clearTimeout(Socket.timeoutID);
        Socket.timeoutID = setTimeout(() => {Socket.getInstance(); Socket.timeoutID = -1;}, 1000);
    }

    static getLink() {
        return Socket.SOCKET_LINK;
    }
}

export default Socket;