$(document).ready(function () {
    updateSuborderTotal();
});

$(document).on("click", "button.close", function () {
    $(this).parent().parent().parent().remove();
    updateSuborderTotal();
})

// Handle adding suborder from order_type field
$("#add-suborder").click(function () {
    let orderType = "&orderType=" + $("#order_type").val()
    $.ajax({
        type: "POST",
        url: "suborder_form",
        data: $("#order-form").serialize() + orderType,
        datatype: "json",
        success: function (result) {
            $("#suborders").html(result);
            updateSuborderTotal();
            $("#suborders .btn-block").last().removeClass("collapsed");
            $("#suborders .panel").last().addClass("show");
        }
    });
    $("#order-type").prop("selectedIndex", 0);
});

function updateSuborderTotal() {
    let suborderTotal = document.querySelectorAll("#suborders table").length;
    $("#suborder-total").html(`Total Suborders: ${suborderTotal}`);
}
