$(function() {
    $('input[type="radio"]').on('click', function(e) {
        var box = $(e.currentTarget).parents('.radio-box');
        box.parents('.radio-container').find('.radio-box').removeClass('selected').addClass('not-selected');
        box.removeClass('not-selected').addClass('selected');
    });
});