$(function () {
    var animationDelay = 50;
    $.each($('.group-container'), function (i, el) {
        setTimeout(function () {
            $(el).removeClass('invisible');
        }, animationDelay * i);
    });

});