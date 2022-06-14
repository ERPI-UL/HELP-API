<template>
    <!-- Admin view page -->
    <div class="min-h-screen flex flex-col bg-gray-900 max-h-screen">
        <div class="p-2"> <!-- Header (with black background) -->
            <Topbar class="bg-gray-800"></Topbar>
        </div>
        <!-- Start main panel -->
        <div class="flex bg-gray-800 m-4 shadow-lg rounded-lg p-2 grow min-h-0">
            <!-- Start user managemenet zone -->
            <div class="flex flex-col rounded-lg p-2 space-y-4 max-w-full border border-gray-600 min-h-0">
                <p class="text-gray-300 text-lg">Utilisateurs</p>
                <!-- User deletion -->
                <div class="flex md:flex-row flex-col md:space-y-0 md:space-x-2 space-y-1 w-full justify-between">
                    <p class="text-gray-400 my-auto">Sélectionner un utilisateur :</p>
                    <select id="user-select" class="min-w-0 border-none rounded bg-gray-700 text-white p-1 pr-8 my-auto">
                        <option value="<loading>">Chargement ...</option>
                    </select>
                    <PaginationChoice :darkMode="true"
                        ref="userPagination" :title="'Sélection utilisateurs'"
                        :selectID="'#user-select'" :callback="addUserSelection" :route="API.ROUTE.USERS"
                        :displayAttribute="el => el.firstname+' '+el.lastname" :identifier="el => el.id" :selectedValues="availableUsers.map(el => el.id)">
                    </PaginationChoice>
                </div>
                <!-- User role modification -->
                <div class="flex md:flex-row flex-col md:space-y-0 md:space-x-2 space-y-1 space-x-0 max-w-full justify-between space-x-4">
                    <p class="text-gray-400 my-auto">Changer le rôle :</p>
                    <select id="role-select" class="min-w-0 border-none rounded bg-gray-700 text-white p-1 pr-8 my-auto">
                        <option value="0">Visiteur</option>
                        <option value="1">Apprenti</option>
                        <option value="2">Enseignant</option>
                        <option value="3">Administrateur</option>
                    </select>
                    <ValidateButton v-on:click="updateUserRole();">Valider</ValidateButton>
                </div>
                <div class="flex flex-col grow justify-end min-h-0">
                    <p class="text-gray-400">Sessions utilisateurs :</p>
                    <div id="user-sessions" class="border rounded-lg border-gray-600 w-full h-full overflow-y-auto overflow-x-hidden min-h-0 max-h-full">
                        
                    </div>
                </div>
                <div class="flex flex-col justify-end">
                    <div class="flex md:flex-row flex-col md:space-y-0 md:space-x-2 space-y-1 space-y-1 w-full h-fit justify-between">
                        <p class="text-gray-400 my-auto mr-4">Supprimer l'utilisateur :</p>
                        <DangerousButton id="delete-user-btn" class="my-auto" v-on:click="deleteUser();">Supprimer</DangerousButton>
                    </div>
                </div>
            </div>
            <!-- End user managemenet zone -->
        </div>
        <!-- End main panel -->

        <!-- Popup debug message zone -->
        <div id="log-message" class="logs-container space-y-2">
            <div class="bg-sky-600"></div> <!-- JUST FOR TAILWIND TO GENERATE COLORS IN CSS -->
            <div class="bg-red-600"></div> <!-- JUST FOR TAILWIND TO GENERATE COLORS IN CSS -->
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import User from "../script/User";
import API from "../script/API";
import PaginationChoice from "../components/PaginationChoice.vue";
import DangerousButton from "../components/DangerousButton.vue";
import ValidateButton from "../components/ValidateButton.vue";

/**
 * Logger class, used to display debug messages in the html popup zone (at the bottom center of the screen)
 */
class Logger {
    static div = null;

    /**
     * Retreives the html popup zone
     */
    static init() {
        Logger.div = document.getElementById("log-message");
    }

    /**
     * Creates a new popup message based on the given message and the popup color
     * @param {string} message popup displayed message
     * @param {string} color popup color
     */
    static createDiv(message, color) {
        if (Logger.div === null) Logger.init();
        const newDiv = document.createElement("div");
        newDiv.className = "text-white w-fit mx-auto slide-in-quick font-semibold text-base text-sm px-3 py-2 rounded-lg shadow-lg bg-"+color+"-600";
        newDiv.innerHTML = (typeof(message)==="string")? message: JSON.stringify(message, null, 2);
        Logger.div.appendChild(newDiv);
        setTimeout(() => {
            newDiv.className += " slide-out-quick";
            setTimeout(() => {newDiv.remove();}, 300);
        }, 3000);
    }

    /**
     * Logs a message in the popup zone
     */
    static log(message) {
        Logger.createDiv(message, "sky");
    }

    /**
     * Logs an error in the popup zone
     */
    static error(message) {
        Logger.createDiv(message, "red");
    }
}

// array containing the users in the delete selection
let availableUsers = [];

/**
 * Updates the delete select html element according to the availableUsersDelete array
 */
function updateUserSelect(selectValue) {
    const userSelect = document.getElementById("user-select");
    let val = userSelect.value;
    userSelect.innerHTML = "";
    const userOptions = [];
    if (availableUsers.length == 0) {
        userOptions.push({value: "", text: "- - - - - - - -"});
        userSelect.value = "";
    }
    availableUsers.forEach(user => userOptions.push(user));
    userOptions.push({value: "<select>", text: "Selectionner ..."});

    userOptions.forEach(option => {
        let optionElement = document.createElement("option");
        optionElement.value = option.value;
        optionElement.text = option.text;
        userSelect.appendChild(optionElement);
    });
    userSelect.value = (val == "" || val == "<loading>" || val == "<select>") ? '<all>': val;
    setTimeout(() => {
        if (selectValue != undefined)
            userSelect.value = selectValue;
        retreiveUserInfos(userSelect.value);
    }, 10);
}

function retreiveUserInfos(userID) {
    const id = parseInt(userID);
    if (isNaN(id)) return;

    // set user role select
    API.execute_logged(API.ROUTE.USERS+userID, API.METHOD_GET, User.currentUser.getCredentials()).then(res => {
        document.getElementById("role-select").value = res.adminLevel;
    }).catch(Logger.error);

    // set user sessions
    loadUserSessions(userID);
}

function loadUserSessions(userID) {
    const container = document.getElementById("user-sessions");
    while (container.firstChild) container.firstChild.remove();

    API.retreiveAll(API.ROUTE.STATS.USERS+userID+API.ROUTE.STATS.__SESSIONS, undefined, true).then(res => {
        res.forEach(s => {
            container.appendChild(createUserSession(s));
        });
    }).catch(Logger.error);
}

function createUserSession(session) {
    const container = document.createElement("div");
    container.classList.add("flex", "flex-col", "grow-0", "h-fit", "p-2", "m-2", "border", "border-gray-700");
    container.innerHTML = `
        <div class="flex grow-0 justify-between">
            <p id="date" class="text-gray-200 text-semibold">${new Date(session.date).toLocaleString()}</p>
            <p id="idSession" class="text-gray-100 text-bold">${session.id}</p>
        </div>
        <p id="scenario" class="text-gray-200 text-semibold">Scenario : ...</p>
        <p id="playedStep" class="text-gray-200 text-semibold">PlayedSteps : ...</p>
        <div class="flex grow justify-end">
            <button class="flex h-fit w-fit whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-red-600 hover:bg-red-700 my-auto">
                Supprimer
            </button>
        </div>
    `;
    setTimeout(() => {
        API.execute_logged(API.ROUTE.STATS.SESSIONS+session.id, API.METHOD_GET, User.currentUser.getCredentials()).then(res => {
            container.querySelector("p#playedStep").innerHTML = "PlayedSteps : "+res.playedSteps.length;
            API.execute_logged(API.ROUTE.SCENARIOS+res.scenario.id, API.METHOD_GET, User.currentUser.getCredentials()).then(scenario => {
                container.querySelector("p#scenario").innerHTML = "Scenario : "+scenario.name;
            }).catch(Logger.error);
        }).catch(Logger.error);

        container.querySelector("button").addEventListener("click", () => {
            API.execute_logged(API.ROUTE.STATS.SESSIONS+session.id, API.METHOD_DELETE, User.currentUser.getCredentials()).then(res => {
                Logger.log("Session "+session.id+" supprimée");
                container.remove();
            }).catch(Logger.error);
        });
    }, 10);
    return container;
}

/**
 * Adds a user to the given content (users list to add) to the availableUsersDelete array (if they are not already in it)
 * And updates the html select element
 */
function addUserSelection(content) {
    availableUsers = availableUsers.filter(el => el.id in content.map(el => el.id));
    let nbAdded = 0, lastSelectedID = 0;
    content.forEach(el => {
        if (!(el.id in availableUsers.map(el => el.id))) {
            nbAdded++;
            lastSelectedID = el.id;
            availableUsers.push({value: el.id, text: el.firstname+" "+el.lastname});
        }
    });
    updateUserSelect((nbAdded==1)? lastSelectedID: undefined);
}

/**
 * Deletes the selected user in the delete html select
 */
function deleteUser() {
    const userSelect = document.getElementById("user-select");
    const userID = parseInt(userSelect.value);
    if (isNaN(userID))
        return;
    Logger.log("Removing user "+userID+" ...");
    API.execute_logged(API.ROUTE.ADMIN.DELETE_USER+userID, API.METHOD_DELETE, User.currentUser.getCredentials()).then(res => {
        Logger.log("User "+userID+" removed");
        availableUsers = availableUsers.filter(el => el.id != userID);
        updateUserSelect();
    }).catch(Logger.error);
}

/**
 * Changes the selected user in the user-role html select for the new role selected in the role html select
 */
function updateUserRole() {
    const userSelect = document.getElementById("user-select");
    const roleSelect = document.getElementById("role-select");
    const userID = parseInt(userSelect.value);
    const roleID = parseInt(roleSelect.value);
    if (isNaN(userID) || isNaN(roleID))
        return;
    Logger.log("Changing user "+userID+" role to "+roleID);
    API.execute_logged(API.ROUTE.CHANGE_ADMIN_LEVEL+userID, API.METHOD_POST, User.currentUser.getCredentials(), {adminLevel: roleID}, API.TYPE_JSON).then(res => {
        Logger.log("User "+userID+" role changed to "+roleID);
    }).catch(Logger.error);
}

export default {
    name: "Admin",
    components: {
        Topbar,
        PaginationChoice,
        DangerousButton,
        ValidateButton
    },
    setup() {
        Logger.init(); // retreive the log html zone
        return {User, API, availableUsers, deleteUser, updateUserRole}
    },
    mounted() {
        if (!User.currentUser.isAdmin()) window.location.href = "/"; // if not admin, go back
        // if the user select is on "Selectionner ..." option, display the user's pagination
        document.getElementById("user-select").addEventListener("change", ev => {
            if (ev.target.value == "<select>") {
                this.$refs["userPagination"].show();
            }
            retreiveUserInfos(ev.target.value);
        });
        
        // update the user selects html elements
        updateUserSelect();
    },
    methods: {addUserSelection}
};
</script>

<style>
.logs-container {
    position: fixed;
    bottom: 50px;
    width: 100vw;
    height: fit-content;
    text-align: center;
}
</style>