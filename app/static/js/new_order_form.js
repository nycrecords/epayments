let suborder_count = 1; // global variable to keep track of the number of new suborders

$(document).ready(function () {
    setClearBtn();
    renderSuborder();
    // setPlaceOrderBtn();
    setPlusBtn();
});

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
        $('#suborder_col').html('')
    });
}

function setPlusBtn() {
    $('#plus_btn').click(function() {
        suborder_count++
        console.log(suborder_count)
        renderSuborder(suborder_count)
        console.log('after setordertypechange')
    })

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
            $('#suborder_col').append(result['suborder_form'])
        }
    })
}