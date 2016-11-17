$(function () {
    $('#add-col').on('click', function () {
        var newCol = $($('.resource-attributes-group')[0]).clone();
        newCol.find('.resource-col-name').val('');
        newCol.find('.resource-col-type').val('');
        newCol.find('.resource-col-descrition').val('');
        $('.resource-attributes-actions').before(newCol);
        $('#remove-col').removeClass('hidden');
    });

    $('#remove-col').on('click', function (e) {
        var cols = $('.resource-attributes-group');
        $(e.currentTarget).toggleClass('hidden', cols.length == 2);
        cols.last().remove()
    });

    function addAttributesHidden() {
        var attributesGroups = $('.resource-attributes-group');
        var attributes = [];
        for (var i = 0; i < attributesGroups.length; i++) {
            var attributeGroupEl = $(attributesGroups[i]);
            var attributeGroup = {
                title: attributeGroupEl.find('.resource-col-name').val(),
                description: attributeGroupEl.find('.resource-col-descrition').val(),
                type: (attributeGroupEl.find('.resource-col-type').val() || '')
            };
            if (attributeGroup.title.length > 0 || attributeGroup.type.length > 0 || attributeGroup.description.length > 0) {
                attributes.push(attributeGroup);
            }
        }
        $('#attributes-description').val(JSON.stringify(attributes));
    }

    $('form#resource-edit').on('submit', function (e) {
        addAttributesHidden();
        return true
    });
});