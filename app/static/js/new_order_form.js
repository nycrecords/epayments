let suborder_count = 1; // global variable to keep track of the number of new suborders

$(document).ready(function () {
    setClearBtn();
    setPlaceOrderBtn();
    setPlusBtn();
    renderSuborder();
});

function setPlaceOrderBtn() {
    $('#place_order_btn').click(function() {
        // gets customer information
        let info = getAllFormsData();
        let order_info = info[0]
        let suborders = info[1]
        placeOrder(order_info, suborders)
    });
}

function getAllFormsData() {
    let order_info;
    let suborders = []
    $('form').each(function (index, form) {
        if (index === 0) { // first form is customer_info
            order_info = convertFormToJSON($('#'+form.id).serializeArray())
        } else {
            let suborder_info = convertFormToJSON($('#'+form.id).serializeArray())
            let type = suborder_info['order_type']
            // only do something if the form is not default type
            if (type !== 'default') {
                suborders[index - 1] = suborder_info;
            }
        }
    });
    return [order_info, suborders]
}

function convertFormToJSON(form_data) {
    let data = {};
    $(form_data).each(function(index, obj){
        data[obj.name] = obj.value;
    });
    return data;
}

function placeOrder(order_info, suborders) {
    console.log('suborders')
    console.log(suborders)
    $.ajax({
        type:'POST',
        url: 'api/v1/orders/new',
        data: JSON.stringify({
            'order_info': order_info,
            'suborders': suborders
        }),
        datatype: 'json',
        success: function(result) {
            console.log('nice')
        }
    });
}

function setClearBtn(){
    $('#clear_btn').click(function() {
        $('#name').val('');
        $('#email').val('');
        $('#address_line_1').val('');
        $('#address_line_2').val('');
        $('#city').val('');
        $('#state').val('');
        $('#zip_code').val('');
        $('#phone').val('');

        // remove all suborders
        suborder_count = 0;
        $('#suborder_col').html('');
    });
}

function setPlusBtn() {
    $('#plus_btn').click(function() {
        suborder_count++;
        renderSuborder();
    });
}

function renderSuborder() {
    $.ajax({
        type: 'POST',
        url: 'newSuborderForm',
        data: JSON.stringify({
            'suborder_count': suborder_count
        }),
        datatype: 'json',
        success: function(result) {
            $('#suborder_col').append(result['suborder_form']);
            setOrderTypeChange(suborder_count); // set order type select field after suborder renders
        }
    });
}

function setOrderTypeChange(suborder_count) {
    let elem_id = 'order_type_' + suborder_count;
    $('#' + elem_id).on('change', function () {
        console.log('changed')
        let type = $('#' + elem_id).val();
        if (type === 'default') // if the option is select an order type
            $('#new_order_fields_' + suborder_count).hide()
        else {
            $('#new_order_fields_' + suborder_count).show()
            orderTypeTemplateRender(type, suborder_count);
        }
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