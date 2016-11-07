$(function () {
    $('.page_primary_action').on('click', '.btn', function () {
        $('.resource-actions').hide();
        $('.spacer').show();
    });
    $('.form-like').on('click', '.form-actions .cancel', function () {
        $('.resource-actions').show();
        $('.spacer').hide();
    }).on('click', '.form-actions .save', function () {
        var saveButton = $('.form-actions .save');
        var interval = setInterval(function () {
            if (!saveButton.hasClass('disabled')) {
                $('.resource-actions').show();
                $('.spacer').hide();
                clearInterval(interval);
            }
        }, 50);
    })
});