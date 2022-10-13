$(document).ready(function () {
    updateSuborderTotal();
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
    let suborderTotal = document.querySelectorAll("#suborders table").length;
    $("#suborder-total").html(`Total Suborders: ${suborderTotal}`);
}

// Handle suborders validation when suborder collapsed
$("#submit").click(function () {
    if ($("#order-form")[0].checkValidity() === false) {
        $(".btn-block").removeClass("collapsed");
        $(".panel").addClass("show");
    }
});
