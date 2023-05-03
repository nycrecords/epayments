$(document).ready(function () {
    updateSuborderTotal();

    $("#clear_button").click(function () {
        clearCustomerForm();
    })
});

$(document).on("click", "button.close", function () {
    $(this).parent().parent().parent().remove();
    updateSuborderTotal();
})

// Handle adding suborder from order_type field
$("#add-suborder").click(function () {
    let orderType = $("#order-type").val();
    if (orderType !== "") {
        $.ajax({
            type: "POST",
            url: "suborder_form",
            data: $("#order-form").serialize(),
            datatype: "json",
            success: function (result) {
                $("#suborders").html(result);
                updateSuborderTotal();
                $("#suborders .btn-block").last().removeClass("collapsed");
                $("#suborders .panel").last().addClass("show");
            }
        });
        $("#order-type").prop("selectedIndex", 0);
    }
});

function updateSuborderTotal() {
    let suborderTotal = document.getElementById("suborders").childElementCount;
    $("#suborder-total").html(`Total Suborders: ${suborderTotal}`);
}

// Handle suborders validation when suborder collapsed
$("#submit").click(function () {
    if ($("#order-form")[0].checkValidity() === false) {
        $(".btn-block").removeClass("collapsed");
        $(".panel").addClass("show");
    }
});

// Clears all customer form inputs
function clearCustomerForm() {
    $("#name").val("");
    $("#email").val("");
    $("#address_line_1").val("");
    $("#address_line_2").val("");
    $("#city").val("");
    $("#state").val("");
    $("#zip_code").val("");
    $("#phone").val("");
}
