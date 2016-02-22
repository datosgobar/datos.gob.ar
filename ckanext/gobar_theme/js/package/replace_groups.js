/*
$(function () {
    var calls = [];
    $('img[data-replace="svg"]').each(function () {
        var $img = $(this);
        var imgURL = $img.attr('src');
        var imgTitle = $img.attr('title');
        calls.push($.get(imgURL, function (data) {
            var $svg = $(data).find('svg').attr('title', imgTitle);
            $img.replaceWith($svg);
        }));
    });
    $.when.apply($, calls).then(function() {
        $('.group-images.invisible').removeClass('invisible');
    });
});

*/