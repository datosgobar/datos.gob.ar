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

    function addGlobalGroupValues() {
        var checkboxList = $('.package-global-group-checkbox:checked');
        var values = [];
        for (var i = 0; i < checkboxList.length; i++) {
            var $checkbox = $(checkboxList[i]);
            values.push($checkbox.attr('id'));
        }
        values = JSON.stringify(values);
        addExtra('global-groups', values)
    }

    var extraCounter = 0;
    function addExtra(key, value) {
        var hiddenKey = $('<input type="hidden">').attr({
            type: 'hidden',
            name: 'extras__' + extraCounter.toString() + '__key',
            value: key
        });
        var hiddenValue = $('<input type="hidden">').attr({
            type: 'hidden',
            name: 'extras__' + extraCounter.toString() + '__value',
            value: value
        });
        var extrasContainer = $('.hidden-extras-container');
        extrasContainer.append(hiddenKey);
        extrasContainer.append(hiddenValue);
        extraCounter += 1;
    }

    function addHiddenExtras() {
        var extras = $('.hidden-extra input, .hidden-extra-select select');
        for (var i = 0; i < extras.length; i++) {
            var extra = $(extras[i]);
            var inputType = extra.attr('type');
            var name = extra.attr('name');
            var value;
            if (inputType == 'text') {
                value = extra.val();
            } else if (inputType == 'checkbox') {
                value = extra.is(':checked').toString()
            } else if (inputType == 'select') {
                var selectedOptions = extra.find('option:selected');
                value = [];
                for (var j = 0; j < selectedOptions.length; j++) {
                    value.push($(selectedOptions[j]).val());
                }
                value = JSON.stringify(value);
                console.log(value);
            }
            addExtra(name, value);
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
        addGlobalGroupValues();
        addHiddenExtras();
        addSaveHidden();
        $form[0].submit();
    })
});