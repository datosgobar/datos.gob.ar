$(function () {
    $('.header-link.dropdown').on('click', function (e) {
        var headerNav = $(e.currentTarget).toggleClass('active');
        e.stopPropagation();
        $('body').one('click', function () {
            headerNav.removeClass('active')
        });
    });
})
