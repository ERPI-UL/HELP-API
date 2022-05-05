<template>
    <div class="min-h-screen flex flex-col bg-black">
        <div class="p-2">
            <Topbar class="bg-gray-800"></Topbar>
        </div>
        <div class="flex bg-gray-800 m-4 shadow-lg rounded-lg p-2 grow">
            <div id="SOCKET-IO" class="w-full flex flex-col">
                <div class="flex justify-between">
                    <h3 class="text-lg font-semibold text-gray-300 text-center m-1">Socket.IO Panel</h3>
                    <input type="text" name="socket-link" id="socket-link" :value="Socket.SOCKET_LINK" class="bg-gray-800 text-white">
                </div>
                <div class="w-fit flex flex-col grow">
                    <div class="border-2 p-2 border-gray-600 rounded-lg">
                        <div class="flex justify-between">
                            <span></span>
                            <h3 class="text-lg font-semibold text-gray-300 text-center m-1">Send event</h3>
                            <button v-on:click="sendEvent" class="bg-indigo-600 px-4 py-1 rounded-lg text-gray-800 font-semibold shadow">Send</button>
                        </div>
                        <div class="flex m-1">
                            <p class="text-gray-300 m-2 whitespace-nowrap">Event name: </p>
                            <input type="text" name="event-name" id="send-event-name" class="size-to-parent bg-gray-800 text-white">
                        </div>
                        <div class="flex m-1">
                            <p class="text-gray-300 m-2">Event data (json): </p>
                            <textarea name="event-data" cols="30" rows="4" id="send-event-content" class="text-white bg-gray-800"></textarea>
                        </div>
                    </div>
                    <div class="border-2 mt-2 p-2 border-gray-600 rounded-lg grow">
                        <div class="flex justify-between">
                            <span></span>
                            <h3 class="text-lg font-semibold text-gray-300 text-center m-1">Received event</h3>
                            <button v-on:click="clearEvents" class="bg-indigo-600 px-4 py-1 rounded-lg text-gray-800 font-semibold shadow">Clear</button>
                        </div>
                        <div id="received-events">
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import Socket from "../script/Socket";
import User from "../script/User";

function sendEvent() {
    const name = document.getElementById("send-event-name");
    const content = document.getElementById("send-event-content");
    Socket.getInstance().emit(name.value, content.value);
    name.value = "";
    content.value = "";
}

function updateSocketEvents() {
    console.log("events: ", socketEvents)
    const parent = document.getElementById("received-events");
    parent.innerHTML = "";
    socketEvents.forEach(ev => {
        parent.innerHTML += `
        <div class="bg-gray-900 m-1 p-1 rounded">
            <div class="flex m-1">
                <p class="text-gray-300 m-2 whitespace-nowrap">Event name: </p>
                <input type="text" name="event-name" id="" value="${ev.eventName}" class="size-to-parent bg-gray-800 text-white">
            </div>
            <div class="flex m-1">
                <p class="text-gray-300 m-2">Event data (json): </p>
                <textarea name="event-data" cols="30" rows="4" class="text-white bg-gray-800">${ev.eventData}</textarea>
            </div>
        </div>\n`;
    });
}

let socketEvents = [];
function clearEvents() {
    socketEvents = [];
    updateSocketEvents();
}

export default {
    name: "Admin",
    components: {
        Topbar
    },
    setup() {
        return {Socket}
    },
    mounted() {
        const user = User.fromJSON(localStorage.getItem("user"));
        if (!user.isAdmin()) window.location.href = "/";

        document.getElementById("socket-link").addEventListener("keyup", ev => {
            if (ev.target.value != Socket.getLink())
                Socket.setLink(ev.target.value);
        });

        Socket.attachSetup(socket => {
            socket.onAny((evName, ...args) => {
                socketEvents.push({eventName: evName, eventData: args});
                updateSocketEvents();
            });
        });
    },
    methods: {sendEvent, clearEvents}
};
</script>
