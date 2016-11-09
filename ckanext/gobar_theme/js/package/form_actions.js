$(function () {
    var $form;

    function addGroupValues() {
        var checkboxList = $('.package-group-checkbox:checked');
        for (var i = 0; i < checkboxList.length; i++) {
            var $checkbox = $(checkboxList[i]);
            var hiddenGroup = $('<input type="hidden">');
            hiddenGroup.attr('name', 'groups__' + i.toString() + '__name');
            hiddenGroup.val($checkbox.attr('id'));
            $form.append(hiddenGroup);
        }
    }

    function addExtra(key, value, number) {
        var hiddenKey = $('<input type="hidden">').attr({
            type: 'hidden',
            name: 'extras__' + number.toString() + '__key',
            value: key
        });
        var hiddenValue = $('<input type="hidden">').attr({
            type: 'hidden',
            name: 'extras__' + number.toString() + '__value',
            value: value
        });
        var extrasContainer = $('.hidden-extras-container');
        extrasContainer.append(hiddenKey);
        extrasContainer.append(hiddenValue);
    }

    function addHiddenExtras() {
        var extras = $('.hidden-extra input');
        for (var i = 0; i < extras.length; i++) {
            var extra = $(extras[i]);
            var inputType = extra.attr('type');
            var name = extra.attr('name');
            var value;
            if (inputType == 'text') {
                value = extra.val();
            } else if (inputType == 'checkbox') {
                value = extra.is(':checked').toString()
            }
            addExtra(name, value, i);
        }
    }

    function addSaveHidden() {
        var hiddenSave = $('<input type="hidden" name="save">');
        $form.append(hiddenSave);
    }

    $('form#dataset-edit').submit(function (e) {
        e.preventDefault();
        $form = $(this);
        addGroupValues();
        addHiddenExtras();
        addSaveHidden();
        $form[0].submit();
    })
});