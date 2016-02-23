$(function () {
    $('form#dataset-edit').submit(function(e) {
        e.preventDefault();
        var $form = $(this);
        var checkboxList = $('.package-group-checkbox:checked');
        for (var i=0; i<checkboxList.length; i++) {
            var $checkbox = $(checkboxList[i]);
            var hiddenGroup = $('<input type="hidden">');
            hiddenGroup.attr('name', 'groups__' + i.toString() + '__name');
            hiddenGroup.val($checkbox.attr('id'));
            $form.append(hiddenGroup);
        }
        $form[0].submit();
    })
});