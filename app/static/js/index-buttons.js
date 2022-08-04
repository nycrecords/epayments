$(document).ready(function () {
    setPassSaveBtn();
    setDownloadBtns();
    showCSVBtn();
})

function setDownloadBtns() {
    setOrderBtn();
    setLargeLabelBtn();
    setSmallLabelBtn();
    setCSVBtn();
}

function printAjaxCall(type) {
    console.log('clicked')
    let c_drs = convertDate($('#date_received_start').val());
    let c_dre = convertDate($('#date_received_end').val());
    let c_srs = convertDate($('#date_submitted_start').val());
    let c_sre = convertDate($('#date_submitted_end').val());
    $.ajax({
        type: 'POST',
        url: 'api/v1/print/' + type,
        data: JSON.stringify({
            'order_number': $("#order_number").val(),
            'suborder_number': $("#suborder_number").val(),
            'order_type': $("#order_type").val(),
            'delivery_method': $("#delivery_method").val(),
            'status': $("#status").val(),
            'billing_name': $("#billing_name").val(),
            'email': $("#email").val(),
            'date_received_start': c_drs,
            'date_received_end': c_dre,
            'date_submitted_start': c_srs,
            'date_submitted_end': c_sre,
        }),
        datatype: 'json',
        success: function (result) {
            window.open(result['url']);
            console.log(result);
        }
    });
}

function setLargeLabelBtn() {
    $('#large_labels').click(function () {
        printAjaxCall('large_labels');
    });
}

function setSmallLabelBtn() {
    $('#small_labels').click(function () {
        printAjaxCall('small_labels');
    });
}

function setOrderBtn() {
    $('#order_sheets').click(function () {
        printAjaxCall('orders')
    });
}

function setPassSaveBtn() {
    $('#pass_submit').click(function () {
        $.ajax({
            type: "PATCH",
            url: "api/v1/password",
            data: JSON.stringify({
                'password': $('#new_pass').val(),
                'confirm_password': $('#confirm_pass').val()
            }),
            datatype: "json",
            success: function (result) {
                alert(result['message']);
                $('#modal_close').click();
            },
            error: function (result) {
                alert(result['responseJSON']['error']['message']);
            }
        });
    });
}

function showCSVBtn() {
    // initial disable when loaded
    $('#xlsx').hide();
    // change csv accessibility everytime order_type is changed
    $('#order_type').on('change', function () {
        if ($('#order_type').val() === 'all') {
            $('#xlsx').hide();
        } else {
            $('#xlsx').show();
        }
    });
}

function setCSVBtn() {
    $('#xlsx').click(function () {
        let c_drs = convertDate($('#date_received_start').val());
        let c_dre = convertDate($('#date_received_end').val());
        let c_srs = convertDate($('#date_submitted_start').val());
        let c_sre = convertDate($('#date_submitted_end').val());

        $.ajax({
            type: "GET",
            url: "api/v1/orders/csv?",
            data: {
                'order_number': $("#order_number").val(),
                'suborder_number': $("#suborder_number").val(),
                'order_type': $("#order_type").val(),
                'delivery_method': $("#delivery_method").val(),
                'status': $("#status").val(),
                'billing_name': $("#billing_name").val(),
                'email': $("#email").val(),
                'date_received_start': c_drs,
                'date_received_end': c_dre,
                'date_submitted_start': c_srs,
                'date_submitted_end': c_sre,
            },
            dataType: "json",
            contentType: "application/json",
            success: function (result) {
                console.log(result)
                window.open(result['url']);
            }
        })
    });
}