import API from "./API";

class User {
    static PERMISSIONS = {
        VISITOR: 0,
        LEARNER: 1,
        TEACHER: 2,
        ADMIN: 3
    }

    static currentUser = User.fromLocalStorage();

    static get USER_ADMIN() {return new User("FurAdmin", "Pawsword", "fur.admin@indico.fr", "Fur", "Admin", {type: "Bearer", token: "fur4dm1nt0k3nuwu"}, User.PERMISSIONS.ADMIN);}
    static get USER_TEACHER() {return new User("FurTeacher", "Pawsword", "fur.teacher@indico.fr", "Fur", "Teacher", {type: "Bearer", token: "furt34ch3rt0k3nuwu"}, User.PERMISSIONS.TEACHER);}
    static get USER_LEARNER() {return new User("FurLearner", "Pawsword", "fur.learner@indico.fr", "Fur", "Learner", {type: "Bearer", token: "furl34rn3rt0k3nuwu"}, User.PERMISSIONS.LEARNER);}

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

    static forgetUser() {
        localStorage.removeItem("user");
        User.curUser = null;
    }

    static fromLocalStorage() {
        const localData = localStorage.getItem("user");
        return localData? User.fromJSON(localData) : new User();
    }

    static refreshUser() {
        User.curUser = User.fromLocalStorage();
    }

    static saveUser(user=User.currentUser) {
        localStorage.setItem("user", User.toJSON(user));
        User.curUser = user;
    }

    static fromJSON(json) {
        if (json == null) return new User();
        if (typeof json === 'string') json = JSON.parse(json);
        return new User(json.username, json.password, json.email, json.firstname, json.lastname, json.token, json.permissions, json.id);
    }

    static toJSON(user) {
        return JSON.stringify(user);
    }

    static sameCredentials(user1, user2) {
        return user1.username === user2.username && user1.password === user2.password;
    }

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
    token = "";
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

    fetchInformations() {
        return new Promise((resolve, reject) => {
            if (!this.token && !(this.username && this.password)) {
                    reject("User not connected");
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
            }).catch(reject);
        });
    }

    getCredentials() {
        return this.token ?? {username: this.username, password: this.password}
    }

    isVisitor() {return this.permissions == User.PERMISSIONS.VISITOR;}
    isTeacher() {return this.permissions == User.PERMISSIONS.TEACHER;}
    isLearner() {return this.permissions == User.PERMISSIONS.LEARNER;}
    isAdmin() {return this.permissions == User.PERMISSIONS.ADMIN;}

    canVisitor() {return this.permissions >= User.PERMISSIONS.VISITOR;}
    canTeacher() {return this.permissions >= User.PERMISSIONS.TEACHER;}
    canLearner() {return this.permissions >= User.PERMISSIONS.LEARNER;}
    canAdmin() {return this.permissions >= User.PERMISSIONS.ADMIN;}

    equals(user) {return this.token.token == user.token.token;}
}

window.User = User; // for debug purposes
export default User;