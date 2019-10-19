$(document).ready(function () {

    var lock = true;
    $.get("http://127.0.0.1:8000/dig",
        {
            "time": gettime(),
            "url": geturl(),
            "refer": getrefer(),
            "userAgent": getuser_agent(),
        },function () {
            lock = false;
        }
        );

})

function gettime() {
    var nowDate = new Date();
    return nowDate.toLocaleString();
}
function geturl() {
    return window.location.href;
}
function getrefer() {
    return document.referrer;
}
function getcookie() {
    return document.cookie;
}
function getuser_agent() {
    return navigator.userAgent;
}