class API {
    static URL = 'http://localhost/api';
    static METHOD_GET = "GET";
    static METHOD_PUT = "PUT";
    static METHOD_POST = "POST";
    static METHOD_PATCH = "PATCH";
    
    static execute(path, method=this.METHOD_GET, body=null, headers=null) {
        return new Promise((resolve, reject) => {
            let reqHeaders = {'Content-Type': 'application/json'};
            if (headers)
                for (let key in headers)
                    reqHeaders[key] = headers[key];

            fetch(API.URL + path, {
                method: method,
                body: (method == this.METHOD_GET)? undefined: body,
                headers: reqHeaders
            }).then(response => {
                if (response.status != 200)
                    reject(response.status);
                else {
                    response.json().then(data => {
                        resolve(data);
                    }).catch(reject);
                }
            }).catch(reject);
        });
    }

    static execute_logged(path, method=this.METHOD_GET, body=null, headers=null) {
        return new Promise((resolve, reject) => {
            const user = localStorage.getItem("user");
            if (!user) {
                reject("User not connected");
                return;
            }
            let reqHeaders = {"token": user.token};
            if (headers)
                for (let key in headers)
                    reqHeaders[key] = headers[key];

            this.execute(path, method, body, reqHeaders).then(resolve).catch(reject);
        });
    }
}

export default API;