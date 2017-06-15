function validLength(length, maxLength) {
    return maxLength >= length;
}

function validTitle(){
    var titleLength = $('input[data-valid-title-length]').val().length;
    var validTitleLength = $('input[data-valid-title-length]').data('valid-title-length');
    return validLength(titleLength, validTitleLength);
}

function validDesc(){
    var descLength = $('textarea[data-valid-desc-length]').val().length
    var validDescLength = $('textarea[data-valid-desc-length]').data('valid-desc-length')
    return validLength(descLength, validDescLength);
}

function validateTitle() {
    $('input#field-title').parent('div').children('div#field-title').toggleClass('long-field', !validTitle());
}

function validateDesc() {
    $('div#field-notes.after-desc').toggleClass('long-field', !validDesc());
}

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

    function formIsValid() {
        $('.missing-field').remove();
        var isValid = true;
        var errorTemplate = '<div class="missing-field">Completá este dato</div>';

        var title = $('#field-title');
        if (!title.val().length > 0) {
            isValid = false;
            title.after(errorTemplate)
        }

        var description = $('#field-notes');
        if (!description.val().length > 0) {
            isValid = false;
            description.after(errorTemplate)
        }

        var author = $('#field-author');
        if (!author.val().length > 0) {
            isValid = false;
            author.after(errorTemplate);
        }

        var updateFreq = $('#update-freq');
        if (!updateFreq.val()) {
            isValid = false;
            updateFreq.after(errorTemplate);
        }

        isFormValid = isValid && validTitle() && validDesc()

        if (!isFormValid) {
             window.scrollTo(0, 0);
             window.scrollTo(0, 0);
         }


        return isFormValid;
    }

    $('form#dataset-edit').submit(function (e) {
        $form = $(this);
        if (formIsValid()) {
            addGroupValues();
            addGlobalGroupValues();
            addHiddenExtras();
            addDates();
            return true
        }
        return false
    });

    $('#save-draft').on('click', function () {
        $('#visibility').val('False');
        $form = $('form#dataset-edit');
        addSaveHidden();
        $form.attr('action', '/dataset/new_draft').submit();
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

    $(document).ajaxComplete(function(){
        $('.slug-preview').each(function() {
            $(this).insertAfter($('div#field-title'));
        });
    });

    $(document).ready(function(){
        $('input[data-valid-title-length]').on('change input keyup', validateTitle)
        validateTitle()


        $('textarea[data-valid-desc-length]').on('change input keyup', validateDesc)
        validateDesc()
     });

    var interval = setInterval(function() {
        var urlPreview = $('.slug-preview');
        if (urlPreview.length > 0) {
            clearInterval(interval);
        }
    }, 100);
});