let suborder_count = 1; // global variable to keep track of the number of new suborders

$(document).ready(function () {
    setClearBtn();
    setPlaceOrderBtn();
    setPlusBtn();
    renderSuborder();
});

function setPlaceOrderBtn() {
    $('#place_order_btn').click(function() {
        // get all inputs from all suborder forms
        $("form").each(function () {
            let inputs = $(this).find(':input')
            console.log(inputs)
            console.log('next')
        });
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
    let elem_id = 'new_order_type_' + suborder_count;
    $('#' + elem_id).on('change', function () {
        console.log('changed')
        let type = $('#' + elem_id).val();
        orderTypeTemplateRender(type, suborder_count);
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