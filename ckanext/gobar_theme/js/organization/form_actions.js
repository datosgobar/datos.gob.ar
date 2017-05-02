$(function () {
    var submit_count = 0;

    function urlValidator(errorTemplate) {
        var url = $('#field-url');
        var urlPreview = $('.slug-preview-value')
        var urlValid = true;
        if ($('.slug-preview').css('display') == 'none'){
            if (!url.val().length > 0) {
                urlValid = false;
                url.parent().after(errorTemplate)
            }
        } else {
            if (urlPreview.text() == '<nombre-de-la-organización>') {
                urlValid = false;
                $('.slug-preview').after(errorTemplate)
            }
        }
        return urlValid;
    }

    function formIsValid() {
        $('.missing-field').remove();
        var titleValid = true;
        var urlValid = true;
        var errorTemplate = '<div class="missing-field">Completá este dato</div>';

        var title = $('#field-name');
        titleValid = title.val().length > 0;

        if (!titleValid){
            title.after(errorTemplate);
        } else {
            urlValid = urlValidator(errorTemplate);
        }

        var isValid = titleValid && urlValid;
        if (!isValid) {
            window.scrollTo(0, 0);
        }

        return isValid;
    }

    $(document).on('click', '.btn-mini', function () {
        if (submit_count > 0){
            return formIsValid();
        }
    });

    $('form#organization-edit-form').submit(function () {
        submit_count++;
        return formIsValid();
    });

});