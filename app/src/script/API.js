class API {
    static API_URL = window.location.protocol+'//indico-api.lf2l.fr';
    static get METHOD_GET() {return "GET";}
    static get METHOD_PUT() {return "PUT";}
    static get METHOD_POST() {return "POST";}
    static get METHOD_PATCH() {return "PATCH";}
    static get TYPE_FORM() {return "application/x-www-form-urlencoded";}
    static get TYPE_JSON() {return "application/json";}
    static get TYPE_NONE() {return undefined;}

    static ROUTE = {
        LOGIN: "/auth/token",
        PASSWORD: "/auth/password",
        USER: "/users/me",
        USERS: "/users/",
        SCENARIOS: "/scenarios/",
        EASY_CONNECT: "/easy/connect"
    };
    
    static execute(path, method=this.METHOD_GET, body=null, type=this.TYPE_NONE, headers=null) {
        return new Promise((resolve, reject) => {
            let reqHeaders = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
                "Accept": "application/json",
                "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"
            };
            if (type != this.TYPE_NONE) reqHeaders["Content-Type"] = type;

            if (headers)
                for (let key in headers)
                    reqHeaders[key] = headers[key];
            let reqBody = type == this.TYPE_FORM ? "": {};
            if (body) {
                switch (typeof(body)) {
                    case "string":
                        if (body.startsWith("{") && body.endsWith("}"))
                            body = JSON.parse(body);
                        // pas de break, pour faire le traitement "object" suivant
                    case "object":
                        if (type == this.TYPE_FORM)
                            reqBody = new URLSearchParams(body).toString();
                        else reqBody = JSON.stringify(body);
                        break;
                    default: break;
                }
            }

            fetch(API.API_URL + path, {
                credentials: "omit",
                method: method,
                body: method == this.METHOD_GET? undefined: reqBody,
                headers: reqHeaders,
                referrer: window.location.origin,
                mode: "cors"
            }).then(response => {
                if (response.status != 200)
                    reject(response);
                else {
                    response.json().then(data => {
                        resolve(data);
                    }).catch(reject);
                }
            }).catch(reject);
        });
    }

    static execute_logged(path, method=this.METHOD_GET, credentials, body=null, type=this.TYPE_NONE, headers=null) {
        return new Promise((resolve, reject) => {
            if (!credentials) {
                reject("Please provide credentials (token/type or username/password)");
                return;
            }
            const login_mode = (credentials.password != undefined && credentials.username != undefined)
            const token_mode = (credentials.token != undefined && credentials.type != undefined)

            if (!login_mode && !token_mode) {
                reject("Error: Invalid credentials");
                return;
            }
            
            let reqHeaders = {};
            if (headers)
                for (let key in headers)
                    reqHeaders[key] = headers[key];

            if (token_mode) {
                reqHeaders.Authorization = credentials.type+" "+credentials.token;
                this.execute(path, method, body, type, reqHeaders).then(resolve).catch(reject);
            } else {
                API.execute("/token", this.METHOD_POST, {username: credentials.username, password: credentials.password}, this.TYPE_FORM).then(data => {
                    reqHeaders.Authorization = data.token_type+" "+data.access_token;
                    this.execute(path, method, body, type, reqHeaders).then(resolve).catch(reject);
                }).catch(reject);
            }
        });
    }

    static createParameters(params) {
        switch (typeof(params)) {
            case "string":
                if (params.startsWith("?")) return params;
                if (params.startsWith("{") && params.endsWith("}"))
                    params = JSON.parse(params);
            case "object":
                return "?" + new URLSearchParams(params).toString();
            default:
                console.error("API Error: Error while creating parameters with argument: ", params);
                return "";
        }
    }

    static createPagination(page, per_page) {
        return this.createParameters({page: page, per_page: per_page});
    }
}

window.API = API; // for debug purposes
export default API;