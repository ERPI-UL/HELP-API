class API {
    // API constants
    static API_URL = window.location.protocol + '//indico-api.lf2l.fr';z
    static get METHOD_GET() { return "GET"; }
    static get METHOD_PUT() { return "PUT"; }
    static get METHOD_POST() { return "POST"; }
    static get METHOD_PATCH() { return "PATCH"; }
    static get METHOD_DELETE() { return "DELETE"; }
    static get TYPE_FORM() { return "application/x-www-form-urlencoded"; }
    static get TYPE_JSON() { return "application/json"; }
    static get TYPE_FILE() { return "multipart/form-data"; }
    static get TYPE_NONE() { return undefined; }
    static get AuthorizationHeader() { return "x-indico-authorization"; };

    // API routes
    static ROUTE = {
        LOGIN: "/auth/token/",
        RESET: "/auth/reset/",
        PASSWORD: "/auth/password/",
        LANGUAGES: "/users/languages/",
        USER: "/users/me/",
        USERS: "/users/",
        INVITE: "/users/invite/",
        SCENARIOS: "/scenarios/",
        EASY_CONNECT: "/easy/connect",
        MACHINES: "/scenarios/machines/",
        CHANGE_ADMIN_LEVEL: "/admin/changeAdminLevel/",
        ADMIN: {
            DELETE_USER: "/admin/deleteUser/",
        },
        __TARGETS: "/targets/",
        __SCENARIOS: "/scenarios/",
        __STEPS: "/steps/",
        __MODEL: "/model/",
        __LANGUAGES: "/languages/",
        STEPS: "/scenarios/steps/",
        STATS: {
            SCENARIOS: {
                AVERAGE_TIME: "/stats/scenarios/averageTime/",
                SKIP_RATE: "/stats/scenarios/skipRate/",
                PERFORM_RATE: "/stats/scenarios/performRate/",
                PERFORM_TIME: "/stats/scenarios/performTime/"
            },
            USERS: "/stats/users/",
            __SESSIONS: "/sessions/",
            SESSIONS: "/stats/sessions/"
        }
    };

    /**
     * Makes an API call with the specified parameters
     * @param {string} path API call url path (see API.ROUTES for possible routes)
     * @param {string} method API call method (see API.METHOD_ for possible values)
     * @param {object|string} body API call body (data to send, ignored if METHOD_GET is used)
     * @param {string} type API call data type (see API.TYPE_ for possible values))  
     * @param {object[]}} headers API call additionnal headers
     * @returns a promise resolving when the API call is done
     */
    static execute(path, method = this.METHOD_GET, body = null, type = this.TYPE_NONE, headers = null) {
        return new Promise((resolve, reject) => {
            // update the API protocol if needed
            if (window.location.protocol !== this.API_URL.split(":")[0]+":")
                this.API_URL = window.location.protocol + '//indico-api.lf2l.fr';

            path = path.replace("/?", "?").replaceAll("//", "/");
            let urlparts = path.split("?");
            let base = urlparts.splice(0, 1);
            let params = (urlparts.length > 0)? ("?" + urlparts.join("&")) : "";
            path = base + params;

            let reqHeaders = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
                "Accept": "application/json",
                "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"
            };
            if (type != this.TYPE_NONE && type != this.TYPE_FILE) reqHeaders["Content-Type"] = type;

            if (headers)
                for (let key in headers)
                    reqHeaders[key] = headers[key];

            let reqBody = type == this.TYPE_FORM ? "" : {};
            if (body && type != this.TYPE_FILE) {
                switch (typeof (body)) {
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

            if (type == this.TYPE_FILE) { // create a form data from the body
                reqBody = new FormData();
                reqBody.append("model", body);
            }
            
            // try with / at the request end
            fetch(API.API_URL + path, {
                credentials: "omit",
                method: method,
                body: method == this.METHOD_GET ? undefined : reqBody,
                headers: reqHeaders,
                referrer: window.location.origin,
                mode: "cors"
            }).then(response => {
                if (response.status != 200)
                    reject({message: response});
                else {
                    response.json().then(data => {
                        resolve(data);
                    }).catch(err => reject({message: err}));
                }
            }).catch(err => {
                // is the request fails, test the same request but without "/" at the end (in case the error it just a 307 shitty redirection)
                fetch(API.API_URL + path.replace("?", "/?"), {
                    credentials: "omit",
                    method: method,
                    body: method == this.METHOD_GET ? undefined : reqBody,
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
                }).catch(err => reject({message: err})).finally(() => {
                });
            });
        });
    }

    /**
     * Makes a logged API call with the specified parameters, using the specified credentials (token + token type / username + password)
     * @param {*} path API call url path (see API.ROUTES for possible routes)
     * @param {*} method API call method (see API.METHOD_ for possible values)
     * @param {*} credentials API call credentials to use (use User.currentUser.getCredentials() to get the current user's credentials)
     * @param {*} body API call body (data to send, ignored if METHOD_GET is used)
     * @param {*} type API call data type (see API.TYPE_ for possible values))
     * @param {*} headers API call additionnal headers
     * @returns A promise resolving when the API call is done
     */
    static execute_logged(path, method = this.METHOD_GET, credentials, body = null, type = this.TYPE_JSON, headers = null) {
        return new Promise((resolve, reject) => {
            if (!credentials) {
                reject({message: "Please provide credentials (token/type or username/password)"});
                return;
            }
            const login_mode = (credentials.password != undefined && credentials.username != undefined)
            const token_mode = (credentials.token != undefined && credentials.type != undefined)

            if (!login_mode && !token_mode) {
                reject({message: "Error: Invalid credentials"});
                return;
            }

            let reqHeaders = {};
            if (headers)
                for (let key in headers)
                    reqHeaders[key] = headers[key];

            if (token_mode) {
                reqHeaders[API.AuthorizationHeader] = credentials.type + " " + credentials.token;
                this.execute(path, method, body, type, reqHeaders).then(resolve).catch(reject);
            } else {
                this.execute(API.ROUTE.LOGIN, this.METHOD_POST, { username: credentials.username, password: credentials.password }, this.TYPE_FORM).then(data => {
                    reqHeaders[API.AuthorizationHeader] = data.token_type + " " + data.access_token;
                    this.execute(path, method, body, type, reqHeaders).then(resolve).catch(reject);
                }).catch(err => reject({message: "Status: "+err.status}));
            }
        });
    }

    /**
     * Retreives all the elements from an API pagination request (User's list for example) [discouraged to use]
     * @param {*} route API route to use (see API.ROUTES for possible routes)
     * @param {*} progressCallback API retreive progression callback (value parameter is from 0 to 1)
     * @param {*} logged Should the API call be logged (use User.currentUser.getCredentials() to get the current user's credentials)
     * @param {*} pageIndex pagination index page to start from
     * @param {*} data original data to add the pagination data to
     * @returns A promise resolving when all the pagination data is retreived (a call to progressCallback will be done just before)
     */
    static retreiveAll(route, progressCallback = p=>{}, logged = false, pageIndex = 1, data = []) {
        return new Promise((resolve, reject) => {
            if (logged) {
                API.execute_logged(route + API.createParameters({ page: pageIndex }), API.METHOD_GET, User.currentUser.getCredentials(), undefined, API.TYPE_JSON).then(res => {
                    if (!res.data) reject("No data found");
                    progressCallback(pageIndex / res.last_page);
                    let dataRetreived = res.current_page == res.last_page;
                    if (!dataRetreived) {
                        API.retreiveAll(route, progressCallback, logged, pageIndex + 1, data.concat(res.data)).then(resolve).catch(reject);
                    }
                    else resolve(data.concat(res.data));
                }).catch(reject);
            }
            else {
                API.execute(route + API.createParameters({ page: pageIndex }), API.METHOD_GET, undefined, API.TYPE_JSON).then(res => {
                    if (!res.data) reject("No data found");
                    progressCallback(pageIndex / res.last_page);
                    let dataRetreived = res.current_page >= res.last_page;
                    if (!dataRetreived)
                        API.retreiveAll(route, progressCallback, logged, pageIndex + 1, data.concat(res.data)).then(resolve).catch(reject);
                    else resolve(data.concat(res.data));
                }).catch(reject);
            }
        });
    }

    /**
     * Creates an iterator for paginated API calls
     * @param {*} path API route to use (see API.ROUTES for possible routes)
     * @param {*} page Page number to start the iterator at
     * @param {*} per_page Number of elements by page
     * @param {*} logged Should the iterator execute API calls with logged mode
     * @returns An object containing the current iterator's call promise and a next function that returns the next iterator object
     */
    static iterate(path, page = 1, per_page = 10, logged = false) {
        let max_page = 1;
        return {
            promise: new Promise((resolve, reject) => {
                API[logged?"execute_logged": "execute"](path + API.createPagination(page, per_page), API.METHOD_GET, logged ? User.currentUser.getCredentials(): undefined)
                    .then(res => {
                        max_page = res.last_page;
                        resolve(res);
                    }).catch(reject);
            }),
            isNext() {
                return page < max_page;
            },
            next() {
                if (page < max_page)
                    return iterate(path, page + 1, per_page);
                else return null;
            }
        };
    }

    /**
     * Creates API parameters from an object
     * @param {object} params key-value pairs of parameters to add to the url
     * @returns string corresponding to the query parameters part of the url
     */
    static createParameters(params) {
        switch (typeof (params)) {
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

    /**
     * Creates pagination parameters from a page index and page number of elements
     * @param {number} page index of the pagination's page
     * @param {number} per_page number of elements in one page
     * @returns a string corresponding to the pagination's parameters part of the url
     */
    static createPagination(page, per_page) {
        return this.createParameters({ page: page, per_page: per_page });
    }
}

window.API = API; // for debug purposes
export default API;