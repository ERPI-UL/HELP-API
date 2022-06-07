/**
 * Redirects the user back in history or on the home page
 * @param {boolean} wait Should the function wait 1s before redirecting
 */
export function redirectHome(wait=true) {
    setTimeout(() => {
        if (document.referrer.startsWith(window.location.origin))
            window.location.href = document.referrer;
        else window.location.href = window.location.origin;
    }, wait?1000:0);
}

/**
 * Converts a number of seconds to a stringified time
 * @param {number} time time in seconds to convert to a string
 * @returns stringified time (minutes+seconds)
 */
export function stringTime(time) {
    let nbMinutes = Math.floor(time / 60);
    let nbSeconds = time % 60;
    return (nbMinutes > 0 ? `${Math.round(nbMinutes)} minute${nbMinutes >= 2 ? "s" : ""} et ` : ``) + `${Math.round(nbSeconds)} seconde${nbSeconds >= 2 ? "s" : ""}`
}

/** FOR EXIT PREVENT POPUP **/
// window.addEventListener("beforeunload", function (e) {
//     var confirmationMessage = "Certaines modifications ne seront pas enregistrés si vous quittez la page maintenant.\n"+
//                               "Enregistrez vos modifications avant de quitter.";
//     (e || window.event).returnValue = confirmationMessage; //Gecko + IE
//     return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
// });