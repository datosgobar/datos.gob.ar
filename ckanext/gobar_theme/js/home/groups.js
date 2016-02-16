$(function () {
    var animationDelay = 50;

    var calls = [];
    $('img[data-replace="svg"]').each(function () {
        var $img = $(this);
        var imgURL = $img.attr('src');
        var imgTitle = $img.attr('title');
        calls.push($.get(imgURL, function (data) {
            var $svg = $(data).find('svg').attr('title', imgTitle);
            $svg.find('style').remove();
            $img.replaceWith($svg);
        }));
    });

    $.when.apply($, calls).then(function () {
        $.each($('.group-container'), function (i, el) {
            setTimeout(function () {
                $(el).removeClass('invisible');
            }, animationDelay * i);
        });
    });
});