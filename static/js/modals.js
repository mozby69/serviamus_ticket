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
    
    
    
     // familychekup
     $("#defaultdatatables").on("click", "tbody .btn_family_checkup", function () {
        var csv_id = $(this).attr('data-ssp-id');
        var branch_name = $(this).attr('data-branch-name'); 


        $.ajax({
            type: 'POST',
            url: '/add_family/',  // URL for Django view handling
            data: {csv_id: csv_id, branch_name:branch_name},
        
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
    
    
    
    
    
    
    
    // ssp personal
    
    $("#defaultdatatables").on("click", "tbody .btn_personal_checkup", function () {
        var csv_id = $(this).attr('data-ssp-id');
        var branch_name = $(this).attr('data-branch-name'); 
    
        $.ajax({
            type: 'POST',
            url: '/add_ssp/',  // URL for Django view handling
            data: {csv_id: csv_id, branch_name:branch_name},
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
    
    
    
    
    $("#defaultdatatables").on("click", "tbody .btn_ticket_list_done", function () {
        var csv_id = $(this).data('ssp-id');
        var name = $(this).data('ssp-name');
        var ticket_ssp_consult = $(this).data('ticket-ssp-consult') || '';
        var ticket_ssp_lab = $(this).data('ticket-ssp-lab') || '';
        var ticket_family_consult = $(this).data('ticket-family-consult') || '';
        var ticket_family_lab = $(this).data('ticket-family-lab') || '';
    
    
        // Construct the ticket display string
        var ticketDisplay = '';
        if (ticket_ssp_consult) {
            ticketDisplay += '<p>SSP Consult Ticket: ' + ticket_ssp_consult + '</p>';
        }
        if (ticket_ssp_lab) {
            ticketDisplay += '<p>SSP Labaratory Ticket: ' + ticket_ssp_lab + '</p>';
        }
        if (ticket_family_consult) {
            ticketDisplay += '<p>Family Consult Ticket: ' + ticket_family_consult + '</p>';
        }
        if (ticket_family_lab) {
            ticketDisplay += '<p>Family Laboratory Ticket: ' + ticket_family_lab + '</p>';
        }
    
        // Update modal content and show it
        $("#ticket_list_modal").modal('show');
        $("#csv_id_tick").val(csv_id);
        $("#display_name").text(name);
        $("#ticket_display").html(ticketDisplay);
    });
    
    
    
    
    // Handling save button click in the modal
    $("#save_ticket_done").on("click", function () {
        var id = $("#csv_id_tick").val();
    
        $.ajax({
            type: 'POST',
            url: '/save_checkup_status/',  // URL for Django view handling
            data: {
                'id': id
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                if (data.success) {
                    Swal.fire({
                        title: "Status successfully changed",
                        text: "SUCCESSFULLY",                                                                  
                        icon: 'success'
                    }).then(function() {
                        window.location.reload(); 
                    });
                } 
                else if (data.warning){
                    Swal.fire({
                        title: "Status Done Already!",
                        text: "Checkup Done!",                                                                  
                        icon: 'warning'
                    }).then(function() {
                        window.location.reload(); 
                    });
                }
                else {
                    Swal.fire({
                        title: "Error Occurred",
                        text: data.message || "ERROR",                                                                  
                        icon: 'error'
                    });
                }
            },
            error: function (xhr, errmsg, err) {
                Swal.fire({
                    title: "An error occurred",
                    text: "Please try again later.",
                    icon: 'error'
                });
            }
        });
    });
    
    
    
    
    
    
    
    
    
   















    // modal table
    $("#defaultdatatable2").on("click", "tbody .btn_table_modal_ticket", function () {
        var data_table_modal_id = $(this).attr('data-table-modal-id');
        var ticket_ssp_consult = $(this).data('ticket-ssp-consult') || '';
        var ticket_ssp_lab = $(this).data('ticket-ssp-lab') || '';
        var ticket_family_consult = $(this).data('ticket-family-consult') || '';
        var ticket_family_lab = $(this).data('ticket-family-lab') || '';



        var ticketDisplay = '';
        if (ticket_ssp_consult) {
            ticketDisplay += "<p style='font-weight:bold;'><span style='color:#266A2C;font-weight:bold;'>SSP CONSULTATION TICKET: &nbsp;</span>" + ticket_ssp_consult + "</p>";

        }
        if (ticket_ssp_lab) {
             ticketDisplay += "<p style='font-weight:bold;'><span style='color:#266A2C;font-weight:bold;'>SSP LABARATORY TICKET: &nbsp;</span>" + ticket_ssp_lab + "</p>";
        }
        if (ticket_family_consult) {
            ticketDisplay += "<p style='font-weight:bold;'><span style='color:#266A2C;font-weight:bold;'>FAMILY CONSULTATION TICKET: &nbsp;</span>" + ticket_family_consult + "</p>";
        }
        if (ticket_family_lab) {
            ticketDisplay += "<p style='font-weight:bold;'><span style='color:#266A2C;font-weight:bold;'>FAMILY LABORATORY TICKET: &nbsp;</span>" + ticket_family_lab + "</p>";
        }
  
        $.ajax({
            type: 'POST',
            url: '/ticket_modal_lists/',  
            data: {data_table_modal_id: data_table_modal_id},
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                if (data.success) {
            
                    $(".view_namess").text(data.name);
                    $("#view_endorsed_to").text(data.endorsed_to);
                    $("#view_relationship").text(data.relationship);
                    $("#view_date_issued").text(formatDate(data.date_issued));
                    $("#view_valid_until").text(formatDate(data.valid_until));
                    $("#view_checkup_status").text(data.checkup_status);
                    $("#view_recepient_type").text(data.recepient_type);
                    $("#view_counter_name").text(data.counter_name);
                    $("#moda_ticket_list").modal('show');
                    $("#ticket_display").html(ticketDisplay);

                } else {
                    alert("error")
                }
            },
            error: function (xhr, errmsg, err) {
                alert("error")
            }
        });
    });


    function formatDate(dateStr) {
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-US', options);
    }


    
    



    // edit view modal


    $("#defaultdatatable2").on("click", "tbody .btn_table_modal_edit", function () {
   
    var data_table_modal_id = $(this).attr('data-table-modal-id');
  
    $.ajax({
        type: 'POST',
        url: '/ticket_modal_lists/',  // URL for Django view handling
        data: {data_table_modal_id: data_table_modal_id},
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (data) {
            if (data.success) {
                // Populate the modal with received data
                $(".edit_id").val(data.id);
                $(".edit_names").val(data.name);
                $(".edit_endorsed_to").val(data.endorsed_to);
                $(".edit_relationship").val(data.relationship);
         
               
                $("#modal_ticket_edit_list").modal('show');
            } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'No Data',
                    text: 'No records found!'
                });
            }
        },
        error: function (xhr, errmsg, err) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something went wrong!'
            });
        }
    });



});
    
    



// save edit modal

$('.update_ssp_modal').submit(function(event) {
    event.preventDefault();

    let formData = new FormData(this);
    // console.log(formData);
    $.ajax({
        type: 'POST',
        url: '/update_table_modal/',
        data: formData,
        processData: false, // Prevent jQuery from automatically transforming the data into a query string
        contentType: false, // Tell jQuery not to set the content type
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(response) {
            if (response.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Data has been succesfully saved!',
                    confirmButtonColor: '#08655D',
                    showConfirmButton: true,
                    confirmButtonText: "Ok"
                }).then(function() {
                    window.location.href = '';
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: response.error_message || 'Something went wrong!'
                });
            }
        },
        error: function(xhr, errmsg, err) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something went wrong!'
            });
        }
    });
});


});