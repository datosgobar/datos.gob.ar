$(function () {
    $('#group-imgs-modal').modal('show');
    $('#group-imgs-modal #select-option').on('click', function () {
        var selectedOption = $('#group-imgs-modal').find('input[name="group-imgs"]:checked').val();
        var options = {'group-imgs': selectedOption, json: true};
        var url = '/configurar/temas';
        var callback = function () { $('#group-imgs-modal').modal('hide'); };
        $.post(url, options, callback);
    });
});