

// $('#data-table').on("click", "#delete-btn", function () {
//     request_id =  $(this).closest("tbody tr").find("dd:eq(0)").html()
//     alert(request_id)
//     swal({
//         title: 'Are you sure?',
//         text: 'Are you sure you want to delete this record?',
//         icon: 'warning',
//         buttons: {
//             cancel: {
//                 text: 'Cancel',
//                 value: null,
//                 visible: true,
//                 className: 'btn btn-default',
//                 closeModal: true,
//             },
//             confirm: {
//                 text: 'Yes',
//                 value: true,
//                 visible: true,
//                 className: 'btn btn-warning',
//                 closeModal: true
//             }
//         }
//     }).then(function (isConfirm) {
//         if (isConfirm) {
//             $.ajax({
//                 type: "POST",
//                 url: "{% url 'id_request_remove' %}",
//                 data:{
//                     request_id: request_id,
//                     csrfmiddlewaretoken: "{{ csrf_token }}",
//                 },
//                 success: function(data){
//                     swal("Success! request has been updated", {
//                           icon: "success",
//                         }).then((willreload) => {
//                             if(willreload){
//                                 window.location.reload()
                                
//                             }
                            
//                         });
//                 },
//                 error: function(error){
//                     console.log(error);
//                 }
            
//             });

//             $.gritter.add({
//                 title: 'Success',
//                 text: 'Record has been deleted',
//                 time: '2000'
//             });
//         }
//     });
// });




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

