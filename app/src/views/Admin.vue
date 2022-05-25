<template>
    <div class="min-h-screen flex flex-col bg-black">
        <div class="p-2">
            <Topbar class="bg-gray-800"></Topbar>
        </div>
        <div class="flex bg-gray-800 m-4 shadow-lg rounded-lg p-2 grow">
            <div class="flex flex-col rounded-lg p-2 space-y-4">
                <p class="text-gray-300 text-lg">Utilisateurs</p>
                <div class="flex flex-col space-y-1">
                    <p class="text-gray-400">Supprimer un utilisateur :</p>
                    <div class="flex space-x-6">
                        <select id="user-select-remove" class="min-w-0 border-none rounded bg-indigo-50 p-1 m-1 pr-8">
                            <option value="<loading>">Chargement ...</option>
                        </select>
                        <DangerousButton v-on:click="deleteUser();">Supprimer</DangerousButton>
                    </div>
                    <PaginationChoice
                        ref="userDeletePagination" :title="'Sélection utilisateurs'"
                        :selectID="'#user-select-remove'" :callback="addUserDeleteSelection" :route="API.ROUTE.USERS"
                        :displayAttribute="el => el.firstname+' '+el.lastname" :identifier="el => el.id" :selectedValues="availableUsersDelete.map(el => el.id)">
                    </PaginationChoice>
                </div>
                <div class="flex flex-col space-y-1">
                    <p class="text-gray-400">Changer le role d'un utilisateur :</p>
                    <div class="flex space-x-6">
                        <select id="user-select-role" class="min-w-0 border-none rounded bg-indigo-50 p-1 m-1 pr-8">
                            <option value="<loading>">Chargement ...</option>
                        </select>
                        <select id="role-select" class="min-w-0 border-none rounded bg-indigo-50 p-1 m-1 pr-8">
                            <option value="0">Visiteur</option>
                            <option value="1">Apprenti</option>
                            <option value="2">Formateur</option>
                            <option value="3">Administrateur</option>
                        </select>
                        <ValidateButton v-on:click="updateUserRole();">Valider</ValidateButton>
                    </div>
                    <PaginationChoice
                        ref="userRolePagination" :title="'Sélection utilisateurs'"
                        :selectID="'#user-select-role'" :callback="addUserRoleSelection" :route="API.ROUTE.USERS"
                        :displayAttribute="el => el.firstname+' '+el.lastname" :identifier="el => el.id" :selectedValues="availableUsersRole.map(el => el.id)">
                    </PaginationChoice>
                </div>
            </div>
        </div>
        <div id="log-message" class="logs-container">
            <!-- JUST FOR TAILWIND TO GENERATE COLORS IN CSS -->
            <div class="bg-sky-600"></div>
            <div class="bg-red-600"></div>
            <!-- JUST FOR TAILWIND TO GENERATE COLORS IN CSS -->
            
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

class Logger {
    div = null;

    static init() {
        this.div = document.getElementById("log-message");
    }

    static createDiv(message, color) {
        if (this.div === null) this.init();
        const newDiv = document.createElement("div");
        newDiv.className = "text-white w-fit mx-auto slide-in-quick font-semibold text-base text-sm px-3 py-2 rounded-lg shadow-lg bg-"+color+"-600";
        newDiv.innerHTML = message;
        this.div.appendChild(newDiv);
        setTimeout(() => {
            newDiv.className += " slide-out-quick";
            setTimeout(() => {newDiv.remove();}, 300);
        }, 3000);
    }

    static log(message) {
        this.createDiv(message, "sky");
    }

    static error(message) {
        this.createDiv(message, "red");
    }
}
window.Logger = Logger;

let availableUsersDelete = [];
function updateUserDeleteSelect(selectValue) {
    const userSelect = document.getElementById("user-select-remove");
    let val = userSelect.value;
    userSelect.innerHTML = "";
    const userOptions = [];
    if (availableUsersDelete.length == 0) userSelect.value = "";
    availableUsersDelete.forEach(user => userOptions.push(user));
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
    }, 10);
}
function addUserDeleteSelection(content) {
    availableUsersDelete = availableUsersDelete.filter(el => el.id in content.map(el => el.id));
    let nbAdded = 0, lastSelectedID = 0;
    content.forEach(el => {
        if (!(el.id in availableUsersDelete.map(el => el.id))) {
            nbAdded++;
            lastSelectedID = el.id;
            availableUsersDelete.push({value: el.id, text: el.firstname+" "+el.lastname});
        }
    });
    updateUserDeleteSelect((nbAdded==1)? lastSelectedID: undefined);
}

let availableUsersRole = [];
function updateUserRoleSelect(selectValue) {
    const userSelect = document.getElementById("user-select-role");
    let val = userSelect.value;
    userSelect.innerHTML = "";
    const userOptions = [];
    if (availableUsersDelete.length == 0) userSelect.value = "";
    availableUsersRole.forEach(user => userOptions.push(user));
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
        document.getElementById("role-select").value = "<loading>";
        API.execute_logged(API.ROUTE.USERS+userSelect.value, API.METHOD_GET, User.currentUser.getCredentials()).then(res => {
            document.getElementById("role-select").value = res.adminLevel;
        }).catch(console.error);
    }, 10);
}
function addUserRoleSelection(content) {
    availableUsersRole = availableUsersRole.filter(el => el.id in content.map(el => el.id));
    let nbAdded = 0, lastSelectedID = 0;
    content.forEach(el => {
        if (!(el.id in availableUsersRole.map(el => el.id))) {
            nbAdded++;
            lastSelectedID = el.id;
            availableUsersRole.push({value: el.id, text: el.firstname+" "+el.lastname});
        }
    });
    updateUserRoleSelect((nbAdded==1)? lastSelectedID: undefined);
}

function deleteUser() {
    const userSelect = document.getElementById("user-select-remove");
    const userID = parseInt(userSelect.value);
    if (isNaN(userID))
        return;
    Logger.log("Removing user "+userID);
    API.execute_logged(API.ROUTE.USERS+userID, API.METHOD_DELETE, User.currentUser.getCredentials()).then(res => {
        Logger.log("User "+userID+" removed");
        availableUsersDelete = availableUsersDelete.filter(el => el.id != userID);
        updateUserDeleteSelect();
    }).catch(Logger.error);
}

function updateUserRole() {
    const userSelect = document.getElementById("user-select-role");
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
        Logger.init();
        return {User, API, availableUsersDelete, availableUsersRole, deleteUser, updateUserRole}
    },
    mounted() {
        if (!User.currentUser.isAdmin()) window.location.href = "/";
        updateUserDeleteSelect();
        document.getElementById("user-select-remove").addEventListener("change", ev => {
            if (ev.target.value == "<select>") {
                this.$refs["userDeletePagination"].show();
            }
        });
        updateUserRoleSelect();
        document.getElementById("user-select-role").addEventListener("change", ev => {
            if (ev.target.value == "<select>") {
                this.$refs["userRolePagination"].show();
            }
        });
    },
    methods: {addUserDeleteSelection, addUserRoleSelection}
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