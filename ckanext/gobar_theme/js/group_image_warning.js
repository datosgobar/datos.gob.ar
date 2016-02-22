$(function () {
    var warningContent = '<span>Warning:</span> la imagen debe ser un svg y no debe tener contenidos ocultos o invisibles';
    var warningEl = $('<p></p>').html(warningContent).addClass('group-warning');
    $('.image-upload').before(warningEl);
});