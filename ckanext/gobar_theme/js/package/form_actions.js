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
        addExtra('globalGroups', values)
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

    function addDates() {
        var dateFrom = $('#date-from').datepicker('getDate');
        var dateTo = $('#date-to').datepicker('getDate');
        if (dateFrom || dateTo) {
            var withHours = $('#date_with_time').is(':checked');
            if (withHours && dateFrom) {
                var hoursFrom = $('#date-from-hour option:selected').val();
                var minutesFrom = $('#date-from-minute option:selected').val();
                dateFrom.setHours(hoursFrom, minutesFrom);
            }
            if (withHours && dateTo) {
                var hoursTo = $('#date-to-hour option:selected').val();
                var minutesTo = $('#date-to-minute option:selected').val();
                dateTo.setHours(hoursTo, minutesTo);
            }
            var value = '';
            if (dateFrom) {
                value = dateFrom.toISOString();
            }
            if (dateTo) {
                value += '/' + dateTo.toISOString();
            }
            addExtra('dateRange', value);
        }
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
                if (extra.attr('multiple') == 'multiple') {
                    var selectedOptions = extra.find('option:selected');
                    value = [];
                    for (var j = 0; j < selectedOptions.length; j++) {
                        value.push($(selectedOptions[j]).val());
                    }
                    value = JSON.stringify(value);
                } else {
                    value = extra.find('option:selected').val();
                }

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
        addDates();
        addSaveHidden();
        $form[0].submit();
    });

    $('#date-from, #date-to').datepicker({
        language: 'es'
    });

    $('#date_with_time').on('change', function (e) {
        var showHours = $(e.currentTarget).is(':checked');
        $('.hour-picker-to, .hour-picker-from').toggleClass('hidden', !showHours);
    });

    var dates = $('.date-picker').data('dates');
    var dateFrom, dateTo;
    if (dates.indexOf('/')) {
        dates = dates.split('/');
        dateFrom = new Date(dates[0]);
        dateTo = new Date(dates[1]);
    } else {
        dateFrom = new Date(dates);
    }
    if (dateFrom instanceof Date && isFinite(dateFrom)) {
        $('#date-from').datepicker('setDate', dateFrom);
        var hoursFrom = dateFrom.getHours();
        var minutesFrom = dateFrom.getMinutes();
        if (hoursFrom != 0 || minutesFrom != 0) {
            hoursFrom = hoursFrom < 10 ? '0' + hoursFrom : hoursFrom.toString();
            minutesFrom = minutesFrom < 10 ? '0' + minutesFrom : minutesFrom.toString();
            $('#date_with_time').prop('checked', true);
            $('.hour-picker-to, .hour-picker-from').removeClass('hidden');
            $('#date-from-hour').val(hoursFrom);
            $('#date-from-minute').val(minutesFrom);
        }
    }
    if (dateTo instanceof Date && isFinite(dateTo)) {
        $('#date-to').datepicker('setDate', dateTo);
        var hoursTo = dateTo.getHours();
        var minutesTo = dateTo.getMinutes();
        if (hoursTo != 0 || minutesTo != 0) {
            hoursTo = hoursTo < 10 ? '0' + hoursTo : hoursTo.toString();
            minutesTo = minutesTo < 10 ? '0' + minutesTo : minutesTo.toString();
            $('#date_with_time').prop('checked', true);
            $('.hour-picker-to, .hour-picker-to').removeClass('hidden');
            $('#date-to-hour').val(hoursTo);
            $('#date-to-minute').val(minutesTo);
        }
    }
});