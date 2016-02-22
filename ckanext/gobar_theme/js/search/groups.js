$(function () {
    var calls = $('.group-images img[data-replace="svg"]').replaceSVG();
    var callback = function () {
        setTimeout(function () {
            $('.search-filter, #search-results').removeClass('invisible')
        }, 200)
    };
    $.when(calls).done(callback).fail(callback);
});
