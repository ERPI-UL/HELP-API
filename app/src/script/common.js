import User from "./User";

/**
 * Converts a number of seconds to a stringified time
 * @param {number} time time in seconds to convert to a string
 * @returns stringified time (minutes+seconds)
 */
export function stringTime(time) {
    let nbMinutes = Math.floor(time / 60);
    let nbSeconds = time % 60;
    let minutes = "";
    if (nbMinutes > 0) {
        minutes = `${Math.round(nbMinutes)} ${nbMinutes >= 2 ? User.LANGUAGE.DATA.TIME.MINUTES : User.LANGUAGE.DATA.TIME.MINUTE}`;
        minutes += ` ${User.LANGUAGE.DATA.COMMON.AND} `;
    }
    let seconds = `${Math.round(nbSeconds)} ${nbSeconds >= 2 ? User.LANGUAGE.DATA.TIME.SECONDS : User.LANGUAGE.DATA.TIME.SECOND}`;
    return (minutes + seconds).toLowerCase();
}


/**
 * Disables an element (and his hover effects)
 * @param {HTMLElement} el element to disable
 */
export function disableEl(el) {
    el.disabled = true;
    el.classList.remove("hover:bg-gray-100");
};

export function CapitalizeObject(obj) {
    switch(typeof obj) {
        case "string":
            return obj.charAt(0).toUpperCase() + obj.slice(1);
            
        case "object":
            for (let key in obj) {
                if (obj.hasOwnProperty(key)) {
                    obj[key] = CapitalizeObject(obj[key]);
                }
            }

        default: break;
    }
    return obj;
}

/** FOR EXIT PREVENT POPUP **/
// window.addEventListener("beforeunload", function (e) {
//     var confirmationMessage = "Certaines modifications ne seront pas enregistrés si vous quittez la page maintenant.\n"+
//                               "Enregistrez vos modifications avant de quitter.";
//     (e || window.event).returnValue = confirmationMessage; //Gecko + IE
//     return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
// });