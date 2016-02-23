$(function () {
    var ua = window.navigator.userAgent;
    var msie = ua.indexOf('MSIE '); // IE 10 or older
    var trident = ua.indexOf('Trident/'); // IE 11

    if (msie > 0 || trident > 0) {
        $('#background-container').css('animation', 'rotateCounterClockwise 300s linear infinite');
    }
});