$(function () {
    var typeIsNumeric = function (fieldType) {
        return ['number', 'integer'].indexOf(fieldType) != -1
    };

    $('#add-col').on('click', function () {
        var newCol = $($('.resource-attributes-group')[0]).clone();
        newCol.find('input, select, textarea').val('');
        newCol.find('.resource-attributes-unit-container').addClass('hidden');
        $('.resource-attributes-actions').before(newCol);
    });

    $(document).on('click', '.remove-col', function (e) {
        var colToRemove = $(e.currentTarget).parents('.resource-attributes-group');
        var isTheOnlyOne = $('.resource-attributes-group').length == 1;
        if (isTheOnlyOne) {
            colToRemove.find('input, select, textarea').val('');
            colToRemove.find('.resource-attributes-unit-container').addClass('hidden');
        } else {
            colToRemove.remove()
        }
    });

    $(document).on('change', '.resource-col-type', function (e) {
        console.log(e);
        var $select = $(e.currentTarget);
        var unitContainer = $select.parents('.other-resource-attributes-container').find('.resource-attributes-unit-container');
        var selectedValue = $select.val();
        var isNumeric = typeIsNumeric(selectedValue);
        if (isNumeric) {
            unitContainer.removeClass('hidden');
        } else {
            unitContainer.addClass('hidden');
        }
    })

    function addAttributesHidden() {
        var attributesGroups = $('.resource-attributes-group');
        var attributes = [];
        for (var i = 0; i < attributesGroups.length; i++) {
            var attributeGroupEl = $(attributesGroups[i]);
            var attributeGroup = {
                title: attributeGroupEl.find('.resource-col-name').val(),
                description: attributeGroupEl.find('.resource-col-descrition').val(),
                type: (attributeGroupEl.find('.resource-col-type').val() || ''),
            };
            if (typeIsNumeric(attributeGroup.type)) {
                attributeGroup.unit = attributeGroupEl.find('.resource-col-unit').val()
            }
            var fieldId = attributeGroupEl.find('.resource-col-id').val();
            if (fieldId) {
                attributeGroup.id = fieldId;
            }
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