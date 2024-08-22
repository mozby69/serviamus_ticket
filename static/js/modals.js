
$(document).ready(function() {
var csrftoken = $('meta[name="csrf-token"]').attr('content');


$("#defaultdatatables").on("click", "tbody .btn_ssp_view", function () {
    var past_ssp_id = $(this).attr('data-ssp-id');

  
    $.ajax({
        type: 'POST',
        url: '/view_ssp/',  // URL for Django view handling
        data: {past_ssp_id: past_ssp_id},
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (data) {
            if (data.success) {
                // Populate the modal with received data
                $("#view_name").text(data.name);
                $("#view_csv_id").text(data.csv_id);
                $("#view_bank").text(data.bank);
                $("#view_add1").text(data.add1);
                $("#view_add2").text(data.add2);
                $("#view_birth").text(data.birth);
                $("#view_ptype").text(data.ptype);
                $("#view_status").text(data.status);
                $("#view_grouping").text(data.grouping);
                $("#view_conmonth").text(data.conmonth);
            
               
                $("#view_ssp_modal").modal('show');
            } else {
                alert("error")
            }
        },
        error: function (xhr, errmsg, err) {
            alert("error")
        }
    });
});








// ssp personal

$("#defaultdatatables").on("click", "tbody .btn_personal_checkup", function () {
    var csv_id = $(this).attr('data-ssp-id');


    $.ajax({
        type: 'POST',
        url: '/add_ssp/',  // URL for Django view handling
        data: {csv_id: csv_id},
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (data) {
            if (data.success) {
      
                $("#name_ssp_type").val(data.name);
                $("#csv_id_ssp_type").val(data.csv_id);

            
               
                $("#ssp_type").modal('show');
            } else {
                alert("error")
            }
        },
        error: function (xhr, errmsg, err) {
            alert("error")
        }
    });
});


// ticket done list
$("#defaultdatatables").on("click", "tbody .btn_ticket_list_done", function () {
    var csv_id = $(this).attr('data-ssp-id');
    var name = $(this).attr('data-ssp-name');

    $("#ticket_list_modal").modal('show');
    $("#display_name").text(data.name)
    document.getElementById("csv_id_tick").value = csv_id;
    document.getElementById("display_name").value = name;

});



$("#save_ticket_done").on("click", function () {
 var x = document.getElementById("csv_id_tick").value;

    $.ajax({
        type: 'POST',
        url: '/save_checkup_status/',  // URL for Django view handling
        data: {x: x},
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (data) {
     
            if (data.success) {
            

                swal.fire({
                    title: "Status successfully changed",
                    text: "SUCCESSFULLY",                                                                  
                    icon: 'success',          
                }).then (function(){
                    window.location.reload(); 
                })           
           
            } else {
                swal.fire({
                    title: "Error Occured",
                    text: "ERROR",                                                                  
                    icon: 'error',          
                });
            }
    
        },
        error: function (xhr, errmsg, err) {
            alert("An error occurred.");
        }
    });


});








// familychekup
$("#defaultdatatables").on("click", "tbody .btn_family_checkup", function () {
    var csv_id = $(this).attr('data-ssp-id');

    $.ajax({
        type: 'POST',
        url: '/add_family/',  // URL for Django view handling
        data: {csv_id: csv_id},
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (data) {
            if (data.success) {
         
                // $("#endorsed_to").val(data.endorsed_to);
                // $("#relationship").val(data.relationship);
                $("#ssp_name_family").text(data.name);
                $("#name_family").val(data.name);
                $("#csv_id_family").val(data.csv_id);

                $("#family_type_modal").modal('show');
            } else {
                alert("No records found.");
            }
        },
        error: function (xhr, errmsg, err) {
            alert("An error occurred.");
        }
    });
});



});






