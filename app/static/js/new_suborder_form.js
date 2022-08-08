$(document).ready(function () {
    setOrderTypeChange(suborder_count) // set action of order_type select field every time a new suborder is added
});

function setOrderTypeChange(suborder_count) {
    let elem_id = 'new_order_type_' + suborder_count
    console.log(elem_id)
    $('#' + elem_id).on('change', function() {
        let type = $('#' + elem_id).val();
        orderTypeTemplateRender(type, suborder_count)
    });
}

function orderTypeTemplateRender(order_type, suborder_count) {
    $.ajax({
        type: 'POST',
        url: 'newSuborder',
        data: JSON.stringify({
            'order_type': order_type,
            'suborder_count': suborder_count,
        }),
        datatype: 'json',
        success: function(result) {
            $('#new_order_fields_' + suborder_count).html(result['template']);
        }
    });
}


