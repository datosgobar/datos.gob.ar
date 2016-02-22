$(function () {
    var animationDelay = 50;
    var calls = $('.featured-groups img[data-replace="svg"]').replaceSVG();
    var callback = function () {
        $.each($('.group-container'), function (i, el) {
            setTimeout(function () {
                $(el).removeClass('invisible');
            }, animationDelay * i);
        });
    };
    $.when(calls).done(callback).fail(callback);
});
