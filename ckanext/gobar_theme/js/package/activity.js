$(function () {
    var activities = $('#pkg-recent-activity').find('li');
    var currentIndex = 5;
    var step = 10;
    var total = parseInt($('ul.activity').data('total'));
    for (var i = 0; i < Math.min(activities.length, currentIndex); i++) {
        $(activities[i]).show();
    }

    var showMoreActivity = function () {
        for (var i = currentIndex; i < Math.min(activities.length, currentIndex + step); i++) {
            $(activities[i]).show();
        }
        currentIndex = i;
    };

    var hideLoading = function () {
        $('.activity-read-more').removeClass('hidden');
        $('.activity-loading').addClass('hidden');
    };

    var showLoading = function () {
        $('.activity-read-more').addClass('hidden');
        $('.activity-loading').removeClass('hidden');
    };

    var pollingForNewActivity = function () {
        activities = $('#pkg-recent-activity').find('li');
        if (activities.length > currentIndex) {
            clearInterval(interval);
            hideLoading();
            showMoreClick();
        }
    };

    var interval;
    var loadMoreActivity = function () {
        var loadMoreButton = $('ul.activity li.load-more');
        if (loadMoreButton.length > 0) {
            loadMoreButton.find('a').click();
            showLoading();
            interval = setInterval(pollingForNewActivity, 200);
        }
    };

    var hideOrShowLoadButton = function () {
        if (total <= currentIndex) {
            $('#pkg-recent-activity').addClass('no-more-activity');
        }
    };

    var showMoreClick = function () {
        activities = $('#pkg-recent-activity').find('li');
        if (activities.length > currentIndex) {
            showMoreActivity();
        } else {
            loadMoreActivity();
        }
        hideOrShowLoadButton();
    };


    $('.activity-read-more').on('click', showMoreClick);
});