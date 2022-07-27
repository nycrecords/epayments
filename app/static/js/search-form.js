$(document).ready(function () {
    $("#applybtn").click(function () {
        getOrders2();
    })

    $("#search_button").click(function () {
        getOrders();
    })

    $("#clear_button").click(function () {
        clearForm();
    })
});

// clears all form inputs
function clearForm() {
    $("#order_number").val("");
    $("#suborder_number").val("");
    $("#order_type").val("all");
    $("#delivery_method").val("all");
    $("#status").val("all");
    $("#billing_name").val("");
    $("#email").val("");
    $("#date_received_start").val("");
    $("#date_received_end").val("");
    $("#date_submitted_start").val("");
    $("#date_submitted_end").val("");
}

// for testing purposes
function getOrders2() {
    $.ajax({
        type: "POST",
        url: "api/v1/orders",
        data: JSON.stringify({
            'order_number': '',
            'suborder_number': '',
            'order_type': 'all',
            'delivery_method': 'all',
            'status': 'all',
            'billing_name': '',
            'date_received_start': '07/18/2022',
            'date_received_end': '07/18/2022',
            'date_submitted_start': '',
            'date_submitted_end': '',
            'start': 0,
            'size': 150
        }),
        datatype: "json",
        success: function (result) {
            createOrderTable(result);
        }
    });
}

// gets the orders with specified fields
function getOrders() {
    // convert the datas from y/m/d -> m/d/y
    let c_drs = convertDate($('#date_received_start').val());
    let c_dre = convertDate($('#date_received_end').val());
    let c_srs = convertDate($('#date_submitted_start').val());
    let c_sre = convertDate($('#date_submitted_end').val());

    $.ajax({
        type: "POST",
        url: "api/v1/orders",
        data: JSON.stringify({
            'order_number': $("#order_number").val(),
            'suborder_number': $("#suborder_number").val(),
            'order_type': $("#order_type").val(),
            'delivery_method': $("#delivery_method").val(),
            'status': $("#status").val(),
            'billing_name': $("#billing_name").val(),
            'email' : $("#email").val(),
            'date_received_start': c_drs,
            'date_received_end': c_dre,
            'date_submitted_start': c_srs,
            'date_submitted_end': c_sre,
            'start': 0,
            'size': 150
        }),
        datatype: "json",
        success: function (result) {
            createOrderTable(result);
        }
    });
}

// create and populate order_rows table with search results
function createOrderTable(data) {
    $.ajax({
        type: 'POST',
        url: "/listorders",
        data: JSON.stringify({
            'all_orders': data['all_orders']
        }),
        datatype: "json",
        success: function (response) {
            $('#total_orders').html('Total orders: ' + data['order_count']);
            $('#total_suborders').html('Total suborders: ' + data['suborder_count']);
            $('#order_rows').html(response['order_rows']);
        }
    });

    // results is a json file
    console.log(data);
}

/**
 * converts date from y/m/d -> m/d/y
 * @param date data that is y/m/d format
 * @returns {string|*} date in m/d/y format
 */
function convertDate(date) {
    if (date === "")
        return date;
    let dateArray = date.split('-');
    let m = dateArray[1];
    let d = dateArray[2];
    let y = dateArray[0];
    return m + '/' + d + '/' + y;
}