let suborderCount = 1
let suborderId = 0
$(document).ready(function () {
    deleteSuborder()
    updateSuborderTotal()
    $("#suborders-0")
});

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
        }
    });
    $("#order-type").prop("selectedIndex", 0);
})

function deleteSuborder(formId) {
    $(`#delete-suborder-btn-${formId}`).click(function () {
        $(`#suborder-${formId}`).remove();
        let counter = 1;
        let suborders = document.querySelectorAll(".suborder-form-label");
        suborders.forEach(function (elem) {
            $(elem).html(`Suborder: ${counter}`);
            counter++;
        });
        suborderCount--
        console.log(suborderCount)
        updateSuborderTotal()
    });
}

function updateSuborderTotal() {
    let suborderTotal = document.getElementById("suborders").children.length
    $("#suborder-total").html(`<h4>Total Suborders: ${suborderTotal}</h4>`)
}
