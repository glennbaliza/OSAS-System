

$('#data-table').on("click", "#delete-btn", function () {
    swal({
        title: 'Are you sure?',
        text: 'Are you sure you want to delete this record?',
        icon: 'warning',
        buttons: {
            cancel: {
                text: 'Cancel',
                value: null,
                visible: true,
                className: 'btn btn-default',
                closeModal: true,
            },
            confirm: {
                text: 'Yes',
                value: true,
                visible: true,
                className: 'btn btn-warning',
                closeModal: true
            }
        }
    }).then(function (isConfirm) {
        if (isConfirm) {
            $.gritter.add({
                title: 'Success',
                text: 'Record has been deleted',
                time: '2000'
            });
        }
    });
});




var handleDataTable = function () {
    "use strict";

    $('#data-table').dataTable({
        responsive: true
    });
};


var table = function () {
    "use strict";
    return {
        init: function () {
            handleDataTable();
        }
    };
}();

