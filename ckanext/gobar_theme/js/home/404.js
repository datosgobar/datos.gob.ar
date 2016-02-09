function dottedDigitsConfig() {
    return [
        [
            [false, true, true, true, false],
            [true, false, false, false, true],
            [true, false, false, false, true],
            [true, false, false, false, true],
            [true, false, false, false, true],
            [false, true, true, true, false]
        ], [
            [false, false, true, false, false],
            [false, true, true, false, false],
            [false, false, true, false, false],
            [false, false, true, false, false],
            [false, false, true, false, false],
            [false, true, true, true, false]
        ], [
            [false, true, true, true, false],
            [true, false, false, false, true],
            [false, false, false, true, false],
            [false, false, true, false, false],
            [false, true, false, false, false],
            [true, true, true, true, true]
        ], [
            [true, true, true, true, true],
            [false, false, false, true, false],
            [false, false, true, false, false],
            [false, false, false, true, false],
            [false, false, false, false, true],
            [false, true, true, true, false]
        ], [
            [false, false, false, true, false],
            [false, false, true, true, false],
            [false, true, false, true, false],
            [true, true, true, true, true],
            [false, false, false, true, false],
            [false, false, false, true, false]
        ], [
            [true, true, true, true, true],
            [true, false, false, false, false],
            [true, true, true, true, false],
            [false, false, false, false, true],
            [false, false, false, false, true],
            [true, true, true, true, false]
        ], [
            [false, false, false, true, false],
            [false, false, true, false, false],
            [false, true, false, false, false],
            [true, true, true, true, true],
            [true, false, false, false, true],
            [false, true, true, true, false]
        ], [
            [false, true, true, true, false],
            [false, false, false, false, true],
            [false, false, false, true, false],
            [false, false, true, false, false],
            [false, false, true, false, false],
            [false, false, true, false, false]
        ], [
            [false, true, true, true, false],
            [true, false, false, false, true],
            [false, true, true, true, false],
            [true, false, false, false, true],
            [true, false, false, false, true],
            [false, true, true, true, false]
        ], [
            [false, true, true, true, false],
            [true, false, false, false, true],
            [true, true, true, true, true],
            [false, false, false, true, false],
            [false, false, true, false, false],
            [false, true, false, false, false]
        ]
    ];
}

function matchedDigitsFor(error) {
    var dottedFont = dottedDigitsConfig();
    var digits = [];
    for (var row = 0; row < 6; row++) {
        for (var i = 0; i < error.length; i++) {
            var digit = parseInt(error[i]);
            digits = digits.concat(dottedFont[digit][row]);
        }
    }
    return digits;
}

function setRedraw() {
    var visibleCircles = $('.circle-background.number-visible');
    var randomCircle = visibleCircles[Math.floor(Math.random() * visibleCircles.length)];
    $(randomCircle).addClass('different').one('click', function (event) {
        var $circle = $(event.currentTarget).parents('.circle');
        $circle.find('.circle-background').removeClass('different');
        fadeOut($circle);
        setTimeout(function() {
            setRedraw();
            fadeIn($circle);
        }, 400);
    });
}

function fadeOut($el) {
    if ($el.hasClass('faded')) {
        return;
    }
    $el.addClass('faded');
    toggleFade($el, fadeOut);
}

function fadeIn($el) {
    if (!$el.hasClass('faded')) {
        return;
    }
    $el.removeClass('faded');
    toggleFade($el, fadeIn);
}

function toggleFade($el, fadeCallback) {
    $el.find('.circle-background').toggleClass('visible');
    var row = parseInt($el.data('row'));
    var col = parseInt($el.data('col'));
    var selectors = '.circle[data-row="' + (row + 1) + '"][data-col="' + col + '"], ' +
        '.circle[data-row="' + (row - 1) + '"][data-col="' + col + '"], ' +
        '.circle[data-row="' + row + '"][data-col="' + (col + 1) + '"],' +
        '.circle[data-row="' + row + '"][data-col="' + (col - 1) + '"]';
    $(selectors).each(function(i, el) {
        setTimeout(function() {
            fadeCallback($(el));
        }, 60)
    })
}

$(function () {
    var error = $('#error-code').data('error').toString();
    var circles = $('.circle-container');
    var digits = matchedDigitsFor(error);
    for (var j = 0; j < circles.length; j++) {
        $(circles[j]).find('.circle-background').toggleClass('visible number-visible', digits[j]);
    }
    setRedraw();
});