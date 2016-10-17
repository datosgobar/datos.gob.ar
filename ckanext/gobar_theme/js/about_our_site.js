function counterAnimation() {
    var totalFrames = 200;
    var counterAnimation = new Vivus('svg-round-counter', {
        duration: totalFrames,
        type: 'async'
    });
    $('#svg-round-counter').show();
    var counterInterval = setInterval(function() {
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
    var totalFrames = 200;
    new Vivus('usalos-svg', {
        duration: totalFrames,
        type: 'async'
    });
    new Vivus('procesalos-svg', {
        duration: totalFrames,
        type: 'async'
    });
    new Vivus('compartilos-svg', {
        duration: totalFrames,
        type: 'async'
    });
    $('#usalos-svg, #compartilos-svg, #procesalos-svg').css('visibility', 'visible')
}

$(function() {
    counterAnimation();
    svgDrawingAnimation();
});