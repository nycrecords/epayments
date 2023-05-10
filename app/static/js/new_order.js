$(document).ready(function () {
    updateSuborderTotal();

    $("#clear_button").on("click", clearCustomerForm);

    $(document).on("click", "button.close", function () {
        $(this).closest(".suborder").remove();
        updateSuborderTotal();
    });

    // Handle adding suborder from order_type field
    $("#add-suborder").on("click", function () {
        let orderType = $("#order-type");
        if (orderType.val() !== "") {
            $.ajax({
                type: "POST",
                url: "suborder_form",
                data: $("#order-form").serialize(),
                datatype: "json",
                success: function (result) {
                    $("#suborders").html(result)
                    updateSuborderTotal();
                    $("#suborders .btn-block").last().removeClass("collapsed");
                    $("#suborders .panel").last().addClass("show");
                }
            });
            orderType.prop("selectedIndex", 0);
        }
    });

    // Handle suborders validation when suborder collapsed
    $("#submit").on("click", function () {
        if ($("#order-form")[0].checkValidity() === false) {
            $(".btn-block").removeClass("collapsed");
            $(".panel").addClass("show");
        }
    });

    function updateSuborderTotal() {
        let suborderTotal = $("#suborders").children().length;
        $("#suborder-total").html(`Total Suborders: ${suborderTotal}`);
    }

    // Clear all customer form inputs
    function clearCustomerForm() {
        $("#name, #email, #address_line_1, #address_line_2, #city, #state, #zip_code, #phone").val("");
    }
});
