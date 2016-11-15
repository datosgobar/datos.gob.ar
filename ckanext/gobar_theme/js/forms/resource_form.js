$(function () {
    $('#add-col').on('click', function () {
        var newCol = $($('.resource-attributes-group')[0]).clone();
        newCol.find('.resource-col-name').val('');
        newCol.find('.resource-col-type').val('');
        newCol.find('.resource-col-descrition').val('');
        $('.resource-attributes-actions').before(newCol);
        $('#remove-col').removeClass('hidden');
    });
    $('#remove-col').on('click', function (e) {
        var cols = $('.resource-attributes-group');
        $(e.currentTarget).toggleClass('hidden', cols.length == 2);
        cols.last().remove()
    });
});