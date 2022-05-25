export function redirectHome(wait=true) {
    setTimeout(() => {
        if (document.referrer.startsWith(window.location.origin))
            window.location.href = document.referrer;
        else window.location.href = window.location.origin;
    }, wait?1000:0);
}

/** FOR EXI PREVENT POPUP **/
// window.addEventListener("beforeunload", function (e) {
//     var confirmationMessage = "Certaines modifications ne seront pas enregistrés si vous quittez la page maintenant.\n"+
//                               "Enregistrez vos modifications avant de quitter.";
//     (e || window.event).returnValue = confirmationMessage; //Gecko + IE
//     return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
// });