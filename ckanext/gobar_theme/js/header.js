$(function () {
    $('.header-link.dropdown').on('click', function (e) {
        var headerNav = $(e.currentTarget).toggleClass('active');
        e.stopPropagation();
        $('body').one('click', function () {
            headerNav.removeClass('active')
        });
    });

    $('#header .icon-reorder').on('click', function(e) {
        $('#header .xs-navbar').toggleClass('hidden')
        $('#header .icon-reorder').toggleClass('active')
        $('#header .logo-header').toggleClass('showing-nav')
    });

    $('#header .dropdown-navbar-link').on('click', function(e) {
        $('#header .dropdown-navbar').toggleClass('hidden')
    })
})
