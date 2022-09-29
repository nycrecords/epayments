let suborder_count = 1

$(document).ready(function () {
    let addSuborderBtn = document.getElementById("add-suborder-btn");
    addSuborderBtn.addEventListener("click", function () {
        getSuborderForm();
    });
});


function getSuborderForm() {
    $.ajax({
        type: 'POST',
        url: 'suborder_form',
        data: JSON.stringify({
            'suborder_count': suborder_count
        }),
        datatype: 'json',
        success: function (result) {
            console.log(result)
            $("#suborders").append(result)
        }
    });
    suborder_count++;
}
