$(function() {
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

});