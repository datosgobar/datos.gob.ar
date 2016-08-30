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

    var hidenKeyFeatured = 'home_featured';
    var extraInputFeatured = $('input[value="home_featured"]');
    if (extraInputFeatured.length > 0) {
        extraInputFeatured.closest('.control-group').remove();
        $('#home_featured').prop('checked', true)
    }

    function addHomeFeaturedValues() {
        if ($('#home_featured').is(':checked')) {
            var extras = $('.control-custom input');
            var maxExtraNum = 0;
            for (var i = 0; i < extras.length; i++) {
                var name = $(extras[i]).attr('name');
                var extraNumber = parseInt(name.split('__')[1]);
                maxExtraNum = Math.max(maxExtraNum, extraNumber);
            }
            maxExtraNum += 1;
            var key = $('<input type="hidden">').attr({
                type: 'hidden',
                name: 'extras__' + maxExtraNum.toString() + '__key',
                value: hidenKeyFeatured
            });
            $form.append(key);
            var value = $('<input type="hidden">').attr({
                type: 'hidden',
                name: 'extras__' + maxExtraNum.toString() + '__value',
                value: 'true'
            });
            $form.append(value);
        }
    }

    var hiddenKeyShortAuthorName = 'Responsable';
    var extraInputShortAuthorName = $('input[value="Responsable"]');
    if (extraInputShortAuthorName.length > 0) {
        shortAuthorNameValue = $('#' + extraInputShortAuthorName.attr('id').replace('key', 'value')).val()
        $('#' + hiddenKeyShortAuthorName).val(shortAuthorNameValue)
        extraInputShortAuthorName.closest('.control-group').remove();
    }

    function addShortAuthorNameValues() {
        var extras = $('.control-custom input');
        var maxExtraNum = 0;
        for (var i = 0; i < extras.length; i++) {
            var name = $(extras[i]).attr('name');
            var extraNumber = parseInt(name.split('__')[1]);
            maxExtraNum = Math.max(maxExtraNum, extraNumber);
        }
        maxExtraNum += 2;
        var key = $('<input type="hidden">').attr({
            type: 'hidden',
            name: 'extras__' + maxExtraNum.toString() + '__key',
            value: hiddenKeyShortAuthorName
        });
        $form.append(key);
        var value = $('<input type="hidden">').attr({
            type: 'hidden',
            name: 'extras__' + maxExtraNum.toString() + '__value',
            value: $('#' + hiddenKeyShortAuthorName).val()
        });
        $form.append(value);
    }    

    $('form#dataset-edit').submit(function (e) {
        e.preventDefault();
        $form = $(this);
        addGroupValues();
        addHomeFeaturedValues();
        addShortAuthorNameValues();
        $form[0].submit();
    })
});