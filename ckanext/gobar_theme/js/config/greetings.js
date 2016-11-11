$(function () {
    $('#greetings-modal').modal('show');
    $('#greetings-modal .dismiss-greetings').on('click', function() {
        $.post('/configurar/mensaje_de_bienvenida', {});
        $('#greetings-modal').modal('hide');
    });
});