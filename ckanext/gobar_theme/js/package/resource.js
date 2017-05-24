$(function () {
    var data = $('#edit-package-container').data();
    $(document).ready(function(){
        if (sessionStorage.getItem('previousUrlCKAN') == null){
            sessionStorage.setItem('previousUrlCKAN', data.refererUrl);
        }
    });
    $('a#back-button').on('click', function(){
        var url;
        if (sessionStorage.getItem('previousUrlCKAN') == ""){
            //Si apretamos volver y luego ponemos en el browser el link de, por ejemplo, resource_data y no se guarda
            //ninguna url en el sessionStorage
            url = data.backUrl;
        } else {
            url = sessionStorage.getItem('previousUrlCKAN');
        }
        sessionStorage.clear();
        window.location.replace(url)
    });
});