$(document).ready(function () {
    setMoreInfoBtns();
    setHistoryBtns();
    setUpdateBtns();
});

function setUpdateBtns() {
    let updateBtn = document.querySelectorAll("[id^='update_btn_']");
    updateBtn.forEach(function (btn) {
        let btnID = btn.getAttribute('id');
        let row_num = btnID.split('_')[2];
        let suborder_number = $('#suborder_' + row_num).attr("data-value");
        // set initial update status option
        let curr_status = $('#status_' + row_num).text();
        $('#updated_status_' + row_num).val(curr_status).change();

        $('#' + btnID).click(function () {
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

function setMoreInfoBtns() {
    let moreInfoBtn = document.querySelectorAll("[id^='moreinfo_btn']");
    moreInfoBtn.forEach(function (btn) {
        let btnID = btn.getAttribute('id');
        let row_num = btnID.split('_')[2];
        let suborder_number = $('#suborder_' + row_num).attr("data-value");
        $('#' + btnID).click(function () {
            $.ajax({
                type: 'POST',
                url: 'api/v1/more_info/' + suborder_number,
                success: function (result) {
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
        });
    });
}

function setHistoryBtns() {
    let historyBtn = document.querySelectorAll("[id^='history_btn']");
    historyBtn.forEach(function (btn) {
        let btnID = btn.getAttribute('id');
        let row_num = btnID.split('_')[2];
        let suborder_number = $('#suborder_' + row_num).attr("data-value");
        $('#' + btnID).click(function () {
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
        });
    });
}