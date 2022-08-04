$(document).ready(function () {
    setMoreInfoBtns();
    setHistoryBtns();
    setUpdateBtns();
    renameStatus();
});

// rename the status to include their description
function renameStatus() {
    let status = document.querySelectorAll("[id^='status_']");
    status.forEach(function (elem) {
        let elem_id = elem.getAttribute('id')
        let row_num = elem_id.split('_')[1]
        let status_info =  $('#updated_status_' + row_num + ' ' + 'option:selected').text().split(':');

        let status = "<strong>" + status_info[0] + "</strong>";
        if (status_info[0] !== 'Received')
            status += ":" + status_info[1];

        $('#' + elem_id).html(status);
    });
}

// sets the update button in update status to submit the update
function setUpdateBtns() {
    let updateBtn = document.querySelectorAll("[id^='update_btn_']");
    updateBtn.forEach(function (btn) {
        let btn_id = btn.getAttribute('id');
        let row_num = btn_id.split('_')[2];
        let suborder_number = $('#suborder_' + row_num).attr("data-value");
        // set initial update status option
        let curr_status = $('#status_' + row_num).text();
        $('#updated_status_' + row_num).val(curr_status).change();

        $('#' + btn_id).click(function () {
            curr_status = $('#status_' + row_num).text();
            let update_status = $('#updated_status_' + row_num).val();
            if (curr_status === update_status) {
                alert('Status was the same. Could not update')
            } else {
                $.ajax({
                    type: 'PATCH',
                    url: 'api/v1/status/' + suborder_number,
                    data: JSON.stringify({
                        'status': update_status,
                        'comment': $('#update_comment_' + row_num).val()
                    }),
                    datatype: 'json',
                    success: function () {
                        alert("Status Has Been Updated");
                        $('#update_comment_' + row_num).val('');
                        $('#status_' + row_num).text(update_status);
                    },
                });
            }
        });
    });
}

// sets the morinfo collapse button to display more info
function setMoreInfoBtns() {
    let moreInfoBtn = document.querySelectorAll("[id^='moreinfo_btn']");
    moreInfoBtn.forEach(function (btn) {
        let btn_id = btn.getAttribute('id');
        let id_array = btn_id.split('_');
        let row_num = id_array[2];
        let suborder_number = $('#suborder_' + row_num).attr("data-value");
        $('#' + btn_id).click(function () {
            if (!$('#' + id_array[0] + '_' + row_num).is(":visible")) {
                $.ajax({
                    type: 'POST',
                    url: 'api/v1/more_info/' + suborder_number,
                    success: function (result) {
                        console.log(result)
                        $.ajax({
                            type: 'POST',
                            url: 'listinfo',
                            data: JSON.stringify({
                                'order_info': result['order_info']
                            }),
                            datatype: 'json',
                            success: function (result) {
                                $('#info_' + row_num).html(result['info_tab']);
                            }
                        });
                    }
                });
            }
        });
    });
}

// sets the history collapse button to display history table
function setHistoryBtns() {
    let historyBtn = document.querySelectorAll("[id^='history_btn']");
    historyBtn.forEach(function (btn) {
        let btn_id = btn.getAttribute('id');
        let id_array = btn_id.split('_');
        let row_num = id_array[2];
        let suborder_number = $('#suborder_' + row_num).attr("data-value");
        $('#' + btn_id).click(function () {
            if (!$('#' + id_array[0] + '_' + row_num).is(":visible")) {
                $.ajax({
                    type: 'GET',
                    url: 'api/v1/history/' + suborder_number,
                    success: function (result) {
                        $.ajax({
                            type: 'POST',
                            url: 'listhistory',
                            data: JSON.stringify({
                                'history': result['history']
                            }),
                            datatype: 'json',
                            success: function (result) {
                                $('#history_body_' + row_num).html(result['history_tab']);
                            }
                        });
                    }
                });
            }
        });
    });
}