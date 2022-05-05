class User {
    static PERMISSIONS = {
        VISITOR: 0,
        LEARNER: 1,
        TEACHER: 2,
        ADMIN: 3
    }

    static USER_ADMIN = new User("FurAdmin", "Pawsword", "fur.admin@indico.fr", "Fur", "Admin", "fur4dm1nt0k3nuwu", User.PERMISSIONS.ADMIN);
    static USER_TEACHER = new User("FurTeacher", "Pawsword", "fur.teacher@indico.fr", "Fur", "Teacher", "furt34ch3rt0k3nuwu", User.PERMISSIONS.TEACHER);
    static USER_LEARNER = new User("FurLearner", "Pawsword", "fur.learner@indico.fr", "Fur", "Learner", "furl34rn3rt0k3nuwu", User.PERMISSIONS.LEARNER);

    static fromJSON(json) {
        if (json == null) return new User();
        if (typeof json === 'string') json = JSON.parse(json);
        return new User(json.username, json.password, json.email, json.firstname, json.lastname, json.token, json.permissions);
    }

    static toJSON(user) {
        return JSON.stringify(user);
    }

    static sameCredentials(user1, user2) {
        return user1.username === user2.username && user1.password === user2.password;
    }

    connected = false;
    username = "";
    password = "";
    email = "";
    firstname = "";
    lastname = "";
    token = "";
    permissions = 0;

    constructor(username="", password="", email="", firstname="", lastname="", token="", permissions=User.PERMISSIONS.VISITOR) {
        this.username = username;
        this.password = password;
        this.email = email;
        this.firstname = firstname;
        this.lastname = lastname;
        this.token = token;
        this.permissions = permissions;
        this.connected = this.username != "";
    }

    isVisitor() {
        return this.permissions == User.PERMISSIONS.VISITOR;
    }

    isTeacher() {
        return this.permissions == User.PERMISSIONS.TEACHER;
    }

    isLearner() {
        return this.permissions == User.PERMISSIONS.LEARNER;
    }

    isAdmin() {
        return this.permissions == User.PERMISSIONS.ADMIN;
    }

    canVisitor() {
        return this.permissions >= User.PERMISSIONS.VISITOR;
    }

    canTeacher() {
        return this.permissions >= User.PERMISSIONS.TEACHER;
    }

    canLearner() {
        return this.permissions >= User.PERMISSIONS.LEARNER;
    }

    canAdmin() {
        return this.permissions >= User.PERMISSIONS.ADMIN;
    }

    equals(user) {
        return this.token == user.token;
    }
}

export default User;