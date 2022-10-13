let suborder_count = 1; // global variable to keep track of the number of new suborders

$(document).ready(function () {
    displaySuborderTotal()
    setClearBtn();
    setPlaceOrderBtn();
    setPlusBtn();
    renderSuborder();
    setSuborderCloseBtn();
});

function setPlaceOrderBtn() {
    $('#place_order_btn').click(function () {
        // gets customer information
        let info = getAllFormsData();
        let order_info = info[0]
        let suborders = info[1]
        if (isValid(order_info, 'customer') && isValid(suborders)) {
            placeOrder(order_info, suborders);
        }
    });
}

function setSuborderCloseBtn(sub_num) {
    $('#suborder_close_btn_' + sub_num).click(function () {
        // remove suborder div
        $('#suborder_' + sub_num).remove();
        // update every suborder number display
        let counter = 1;
        let suborder_displays = document.querySelectorAll("[id^='suborder_num_']");
        suborder_displays.forEach(function (elem) {
            $('#' + elem.id).html('Suborder: ' + counter)
            counter++;
        });
        suborder_count--;
        displaySuborderTotal();
    });
}

function displaySuborderTotal() {
    $('#total_new_suborders').html('Total New Suborders: ' + suborder_count)
}

// gets all the form data from the customer form and all new suborder forms
function getAllFormsData() {
    let order_info;
    let suborders = []
    $('form').each(function (index, form) {
        if (index === 0) { // first form is customer_info
            order_info = convertFormToJSON($('#' + form.id).serializeArray())
        } else {
            let suborder_info = convertFormToJSON($('#' + form.id).serializeArray())
            let type = suborder_info['order_type']
            // only do something if the form is not default type
            if (type !== 'default') {
                suborders[index - 1] = suborder_info;
            }
        }
    });
    return [order_info, suborders]
}

function isValid(form, form_type='suborder') {
    if (form_type === 'suborder') {
        return form.length !== 0 && form['order_type'] === 'default';
    }
    else {
        // pattern matches (string)@(string).(domain 2-3 letters)
        let email_pattern = new RegExp('[a-z0-9]+@[a-z]+\.[a-z]{2,3}');
        let email = form['email'];
        let is_valid = email_pattern.test(email)
        if (!is_valid)
            alert('Invalid Email')
        return is_valid;
    }
}

function convertFormToJSON(form_data) {
    let data = {};
    $(form_data).each(function (index, obj) {
        data[obj.name] = obj.value;
    });
    return data;
}

function placeOrder(order_info, suborders) {
    if (suborders.length > 0) {
        $.ajax({
            type: 'POST',
            url: 'api/v1/orders/new',
            data: JSON.stringify({
                'order_info': order_info,
                'suborders': suborders
            }),
            datatype: 'json',
            success: function (result) {
                alert('Order Placed')
            }
        });
    } else {
        alert('There are no suborders to place')
    }
}

function setClearBtn() {
    $('#clear_btn').click(function () {
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
        displaySuborderTotal()
    });
}

function setPlusBtn() {
    $('#plus_btn').click(function () {
        suborder_count++;
        displaySuborderTotal()
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
        success: function (result) {
            $('#suborder_col').append(result['suborder_form']);
            setOrderTypeChange(suborder_count); // set order type select field after suborder renders
            setSuborderCloseBtn(suborder_count);
        }
    });
}

function setOrderTypeChange(suborder_count) {
    let elem_id = 'order_type_' + suborder_count;
    $('#' + elem_id).on('change', function () {
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
        success: function (result) {
            $('#new_order_fields_' + suborder_count).html(result['template']);
        }
    });
}