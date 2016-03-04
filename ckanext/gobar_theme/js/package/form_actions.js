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

    var hidenKey = 'home_featured';
    var extraInput = $('input[value="home_featured"]');
    if (extraInput.length > 0) {
        extraInput.closest('.control-group').remove();
        $('#home_featured').prop('checked', true)
    }

    function addHomeFeaturedValues() {
        if ($('#home_featured').is(':checked')) {
            var extras = $('.control-custom input');
            var maxExtraNum = 0;
            for (var i = 0; i < extras.length; i++) {
                var name = $(extras[i]).attr('name');
                var extraNumber = parseInt(name.split('__')[1]);
                console.log(extraNumber);
                maxExtraNum = Math.max(maxExtraNum, extraNumber);
            }
            maxExtraNum += 1;
            var key = $('<input type="hidden">').attr({
                type: 'hidden',
                name: 'extras__' + maxExtraNum.toString() + '__key',
                value: hidenKey
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

    $('form#dataset-edit').submit(function (e) {
        e.preventDefault();
        $form = $(this);
        addGroupValues();
        addHomeFeaturedValues();
        $form[0].submit();
    })
});