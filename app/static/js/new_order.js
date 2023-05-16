$(document).ready(function () {
    updateSuborderTotal();
    setCopiesVisibility();

    $(document).on("click", "button.close", function () {
        $(this).closest(".suborder").remove();
        updateSuborderTotal();
    });

    function updateSuborderTotal() {
        let suborderTotal = $("#suborders").children().length;
        $("#suborder-total").html(`Total Suborders: ${suborderTotal}`);
    }

    // Clear all customer form inputs
    function clearCustomerForm() {
        $("#name, #email, #address_line_1, #address_line_2, #city, #state, #zip_code, #phone").val("");
    }

    $("#clear_button").on("click", clearCustomerForm);

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

    // Format customer phone
    document.getElementById('phone').addEventListener('input', function (e) {
        let x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
    });

    // Handle visibility of number of copies option when exemplification, raised_seals, or no_amends is checked
    function setCopiesVisibility() {
        let checkboxes = document.querySelectorAll("#suborders input[type='checkbox']");

        checkboxes.forEach(function (checkbox) {
            setCheckbox(checkbox)
        });

        function setCheckbox(checkbox) {
            let copiesInput = $(`#${checkbox.id}_copies`);
            let copiesLabel = $(`label[for="${checkbox.id}_copies"]`);
            let isChecked = checkbox.checked;

            copiesInput.toggle(isChecked).attr('required', isChecked);
            copiesLabel.toggle(isChecked).attr('required', isChecked);
            if (!isChecked) {
                copiesInput.val('');
            }
        }

        $('#suborders, input[type="checkbox"]').click(function (event) {
            setCheckbox(event.target)
        });
    }
});
