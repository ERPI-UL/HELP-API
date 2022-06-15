import API from "./API";
import English from "../assets/languages/English";
import French from "../assets/languages/French";
import { CapitalizeObject } from "../script/common";

/**
 * User class, used to store user information.
 */
class User {
    static get AVAILABLE_LANGUAGES() { return [
        {
            NAME: "English",
            CODE: "en",
            FLAG: "🇬🇧",
            DATA: CapitalizeObject(English)
        },
        {
            NAME: "Français",
            CODE: "fr",
            FLAG: "🇫🇷",
            DATA: CapitalizeObject(French)
        }
    ];};

    static LANGUAGE = this.AVAILABLE_LANGUAGES[0];

    static LoadLanguage(language) {
        if (!language) return; // no language set, no need to load anything

        if (typeof(language) == "string") { // language code, get the language object from it
            this.LoadLanguage(this.AVAILABLE_LANGUAGES.find(l => l.CODE === language) ?? this.AVAILABLE_LANGUAGES.find(l => l.NAME === language));
            return;
        }
        if (language.CODE) { // language object, load it
            localStorage.setItem("language", language.CODE);
            User.LANGUAGE = language;
        }
    }

    // User available permissions
    static PERMISSIONS = {
        VISITOR: 0,
        LEARNER: 1,
        TEACHER: 2,
        ADMIN: 3
    }

    // User current (default at what's in the localstorage)
    static currentUser = User.fromLocalStorage();

    /**
     * Retreives the user's informations in the token and creates a new user with them
     * @param {string|object} token token object or string containing type and token fields
     * @returns a new user created from the given token object or string
     */
    static fromToken(token) {
        if (token == null) return new User();
        if (typeof token === 'string') token = JSON.parse(token);
        if (!token.type || !token.token) {
            console.error("Error gettings user from token: missing token fields (type, token)");
            return new User();
        }
        try {
            const tokenInfos = JSON.parse(atob(token.token.split(".")[1]));
            return new User(tokenInfos.username??"", "", "", "", "", {type: token.type, token: token.token}, tokenInfos.adminLevel??User.PERMISSIONS.VISITOR, tokenInfos.id??0);
        } catch(e) {
            console.error("Error getting user from token"+e);
            return new User();
        }
    }

    /**
     * Removes all user informations from the client
     */
    static forgetUser() {
        localStorage.removeItem("user");
        User.curUser = null;
    }

    /**
     * Returns the user stored in the client's localstorage (new User is null)
     * @returns {User} The user corresponding to the state of the client's local storage
     */
    static fromLocalStorage() {
        const localData = localStorage.getItem("user");
        return localData? User.fromJSON(localData) : new User();
    }

    /**
     * Retreives the user from the localstorage and replaces the current one by the new retreived one
     */
    static refreshUser() {
        User.curUser = User.fromLocalStorage();
    }

    /**
     * Saves a user in the client's localstorage
     * @param {User} user user to save to the localstorage
     */
    static saveUser(user=User.currentUser) {
        localStorage.setItem("user", User.toJSON(user));
        User.curUser = user;
    }

    /**
     * Creates a user from the given JSON string or object
     * @param {string|object} json json object to use to create the user from
     * @returns the user created from the given JSON string or object
     */
    static fromJSON(json) {
        if (json == null) return new User();
        if (typeof json === 'string') json = JSON.parse(json);
        return new User(json.username, json.password, json.email, json.firstname, json.lastname, json.token, json.permissions, json.id);
    }

    /**
     * Converts a user to a JSON string
     * @param {User} user user to convert to JSON
     * @returns json string representing the user
     */
    static toJSON(user) {
        return JSON.stringify(user);
    }

    /**
     * Compares two user's credentials and returns true if they are the same
     * @param {User} user1 first user
     * @param {User} user2 second user
     * @returns if the user's credentials are the same
     */
    static sameCredentials(user1, user2) {
        return user1.username === user2.username && user1.password === user2.password;
    }

    /**
     * Checks if a given user is connected or not
     * @param {User} user user to test
     * @returns if the user is connected is connected or not
     */
    static isConnected(user) {
        return !(user == null || user.username == null || user.username == "");
    }

    verified = false;
    id = 0;
    username = "";
    password = "";
    email = "";
    firstname = "";
    lastname = "";
    token = null;
    permissions = 0;

    constructor(username="", password="", email="", firstname="", lastname="", token=null, permissions=User.PERMISSIONS.VISITOR, id=0) {
        this.id = id;
        this.username = username;
        this.password = password;
        this.email = email;
        this.firstname = firstname;
        this.lastname = lastname;
        this.token = token;
        this.permissions = permissions;
    }

    /**
     * Fetches all the user's informations from the server with an API call
     * @returns {Promise} a promise containing the user's informations, resolving when the API call is done
     */
    fetchInformations(debugFunction=m=>{}) {
        return new Promise((resolve, reject) => {
            if (!this.token && !(this.username && this.password)) {
                    reject({message: "Fetch error : User not connected"});
                    return;
            }
            API.execute_logged(API.ROUTE.USER, API.METHOD_GET, this.getCredentials()).then(data => {
                this.id = data.id;
                this.username = data.username;
                this.email = data.email;
                this.firstname = data.firstname;
                this.lastname = data.lastname;
                this.permissions = data.adminLevel;
                this.verified = true;
                User.forgetUser();
                User.saveUser(this);
                resolve(this);
            }).catch(err => {reject({message: err.message})});
        });
    }

    /**
     * Returns the credentials corresponding to this user
     * @returns The credentials of the user
     */
    getCredentials() {
        return this.token ?? {username: this.username, password: this.password}
    }

    // is the user a visitor
    isVisitor() {return this.permissions == User.PERMISSIONS.VISITOR;}
    // is the user a teacher
    isTeacher() {return this.permissions == User.PERMISSIONS.TEACHER;}
    // is the user a learner
    isLearner() {return this.permissions == User.PERMISSIONS.LEARNER;}
    // is the user an admin
    isAdmin() {return this.permissions == User.PERMISSIONS.ADMIN;}

    // does the user have visitor permissions (or above)
    canVisitor() {return this.permissions >= User.PERMISSIONS.VISITOR;}
    // does the user have teacher permissions (or above)
    canTeacher() {return this.permissions >= User.PERMISSIONS.TEACHER;}
    // does the user have learner permissions (or above)
    canLearner() {return this.permissions >= User.PERMISSIONS.LEARNER;}
    // does the user have admin permissions (or above)
    canAdmin() {return this.permissions >= User.PERMISSIONS.ADMIN;}

    // is the user equal to another user (compares the tokens)
    equals(user) {return this.token.token == user.token.token;}
}

// LANGUAGE SETUP
const language = localStorage.getItem("language");
if (language) User.LoadLanguage(language);

window.User = User; // for debug purposes
export default User;