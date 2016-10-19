function counterAnimation() {
    var totalFrames = 200;
    var counterAnimation = new Vivus('svg-round-counter', {
        duration: totalFrames,
        type: 'async'
    });
    $('#svg-round-counter').show();
    var counterInterval = setInterval(function () {
        if (counterAnimation.currentFrame >= totalFrames) {
            clearInterval(counterInterval);
            $('.counter-number').text('100%');
        } else {
            var progress = counterAnimation.currentFrame / totalFrames;
            var percentageProgress = Math.ceil(progress * 100);
            $('.counter-number').text(percentageProgress + '%');
        }
    }, 50);

}

function svgDrawingAnimation() {
    var showWhenVisible = function (name) {
        var vivusOptions = {
            duration: 200,
            type: 'async'
        };
        var visSenseOptions = {fullyvisible: 0.8};
        var container = $('#' + name + '-container');
        var visibility = VisSense(container[0], visSenseOptions);
        var monitor = visibility.monitor({
            fullyvisible: function () {
                new Vivus(name + '-svg', vivusOptions);
                $('#' + name + '-svg').css('visibility', 'visible');
                monitor.stop();
            }
        });
        monitor.start();
    };

    showWhenVisible('usalos');
    showWhenVisible('compartilos');
    showWhenVisible('procesalos');
}

function stepsAnimation() {
    var fadeWhenVisible = function(name, fadeType) {
        var container = $('#' + name + '-container');
        var visSenseOptions = {fullyvisible: 0.8};
        var visibility = VisSense(container[0], visSenseOptions);
        var monitor = visibility.monitor({
            fullyvisible: function () {
                $('#' + name + '-svg').css('visibility', 'visible').attr('class', 'animated ' + fadeType);
                monitor.stop();
            }
        });
        monitor.start();
    };
    fadeWhenVisible('transparencia', 'fadeInRight');
    fadeWhenVisible('comunidad', 'fadeInLeft');
    fadeWhenVisible('kit', 'fadeInRight');
}

$(function () {
    counterAnimation();
    //svgDrawingAnimation();
    stepsAnimation();
});