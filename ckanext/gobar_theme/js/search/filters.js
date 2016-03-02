$(function () {
    $('.menu-button').on('click', function () {
        $('.filters-container').addClass('side-visible');
        $('#search-results').addClass('hidden-by-filters');
    });
    $('.hide-filters-button').on('click', function () {
        $('.filters-container').removeClass('side-visible');
        $('#search-results').removeClass('hidden-by-filters');
    })
});