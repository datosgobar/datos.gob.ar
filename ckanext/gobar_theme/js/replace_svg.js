$(function () {
    function replaceSVG(el) {
        var $img = $(el);
        var imgURL = $img.attr('src');
        var imgTitle = $img.data('title');
        var imgClass = $img.attr('class');
        var requestParams = {
            url: imgURL,
            method: 'GET',
            error: function () {
                $(document).trigger('svg:replace:error', $img);
            },
            success: function (data) {
                try {
                    var $svg = $(data).find('svg').attr('class', imgClass);
                    var tooltipText = $('<div></div>').text(imgTitle).addClass('tooltip-text');
                    var tooltip = $('<div></div>').addClass('svg-tooltip').append(tooltipText);
                    $img.replaceWith($svg);
                    $svg.after(tooltip);
                    $(document).trigger('svg:replace:success', $svg);
                }
                catch (err) {
                    $(document).trigger('svg:replace:error', $img);
                }
            }
        };
        return $.ajax(requestParams);
    }

    $.fn.extend({
        replaceSVG: function () {
            return $.map(this, replaceSVG);
        }
    });

});