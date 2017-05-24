$(function () {
    function formIsValid() {
        $('.missing-field').remove();
        var isValid = true;
        var errorTemplate = '<div class="missing-field">Completá este dato</div>';

        var title = $('#field-name');
        if (title.val().length == 0){
            isValid = false;
            title.after(errorTemplate)
        }

        if (!isValid) {
            window.scrollTo(0, 0);
        }
        return isValid;
    }

    $('form#resource-edit').submit(function () {
        return formIsValid();
    });

});