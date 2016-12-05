$(function() {
    $('input[type="file"]').on('change', function(e) {
        var fileInput = $(e.currentTarget);
        fileInput.siblings('.filename-input').val(fileInput.val());
        var container = fileInput.parents('.file-upload-container').addClass('with-image');
        container.find('#image-logic').val('new-image');
    });

    $('.icon-remove-sign').on('click', function(e) {
        var container = $(e.currentTarget).parents('.file-upload-container').removeClass('with-image');
        var fileInput = container.find('#background-image');
        fileInput.replaceWith(fileInput.val('').clone(true));
        container.find('.filename-input').val('');
        container.find('#image-logic').val('delete-image')
    })
});