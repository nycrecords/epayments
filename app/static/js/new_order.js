$(document).ready(function () {
    updateSuborderTotal();
    setCopiesVisibility();
    attachEventHandlers();

    function updateSuborderTotal() {
        let suborderTotal = $("#suborders").children().length;
        $("#suborder-total").html(`Total Suborders: ${suborderTotal}`);
    }

    // Clear all customer form inputs
    function clearCustomerForm() {
        $("#name, #address_line_1, #address_line_2, #city, #state, #zip_code, #phone, #email").val("");
        $("#country").val("United States");
    }

    // Handle adding suborder from order_type field
    function addSuborder() {
        let orderType = $("#order-type");
        if (orderType.val() !== "") {
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
            orderType.prop("selectedIndex", 0);
        }
    }

    // Handle suborders validation when suborder collapsed
    function suborderValidation() {
        if ($("#order-form")[0].checkValidity() === false) {
            $(".btn-block").removeClass("collapsed");
            $(".panel").addClass("show");
        }
    }

    function formatPhoneNumbers(phoneInput) {
        phoneInput.addEventListener('input', function (e) {
            let x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
            e.target.value = !x[2] ? x[1] : `(${x[1]}) ${x[2]}${x[3] ? '-' + x[3] : ''}`;
        });
    }

    function formatTotal(totalInput) {
        totalInput.value = parseFloat(totalInput.value).toFixed(2);
    }

    // Handle visibility of number of copies option when exemplification, raised_seals, or no_amends is checked
    function setCopiesVisibility() {
        $("#suborders").on("click", "input[type='checkbox']", function () {
            let copiesInput = $(`#${this.id}_copies`);
            let copiesLabel = $(`label[for="${this.id}_copies"]`);
            let isChecked = this.checked;

            copiesInput.toggle(isChecked).attr('required', isChecked);
            copiesLabel.toggle(isChecked).attr('required', isChecked);

            if (!isChecked) {
                copiesInput.val('');
            }
        });
    }

    function attachEventHandlers() {
        let suborders = $("#suborders")

        suborders.on("click", "button.close", function () {
            $(this).closest(".suborder").remove();
            updateSuborderTotal();
        });

        suborders.on("click", "input[id*='contact_num']", function () {
            formatPhoneNumbers(this);
        });

        suborders.on("blur", "input[id*='total']", function () {
            formatTotal(this);
        });

        $("#phone").on("click", function () {
            formatPhoneNumbers(this);
        });

        $("#clear_button").on("click", clearCustomerForm);
        $("#add-suborder").on("click", addSuborder);
        $("#submit").on("click", suborderValidation);
    }
});
