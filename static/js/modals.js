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
    
    
    
    
    $("#defaultdatatables").on("click", "tbody .btn_ticket_list_done", function () {
        var csv_id = $(this).data('ssp-id');
        var name = $(this).data('ssp-name');
        var ticket_ssp_consult = $(this).data('ticket-ssp-consult') || '';
        var ticket_ssp_lab = $(this).data('ticket-ssp-lab') || '';
        var ticket_family_consult = $(this).data('ticket-family-consult') || '';
        var ticket_family_lab = $(this).data('ticket-family-lab') || '';
    
        // Log the values to the console for debugging
        console.log("CSV ID: " + csv_id);
        console.log("Name: " + name);
        console.log("SSP Consult Ticket: " + ticket_ssp_consult);
        console.log("SSP Lab Ticket: " + ticket_ssp_lab);
        console.log("Family Consult Ticket: " + ticket_family_consult);
        console.log("Family Lab Ticket: " + ticket_family_lab);
    
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
        var csv_id = $("#csv_id_tick").val();
    
        $.ajax({
            type: 'POST',
            url: '/save_checkup_status/',  // URL for Django view handling
            data: {
                'x': csv_id
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
                } else {
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
    
    
    
    
    
    
    
    
    
    // familychekup
    $("#defaultdatatables").on("click", "tbody .btn_family_checkup", function () {
        var csv_id = $(this).attr('data-ssp-id');
    
        $.ajax({
            type: 'POST',
            url: '/add_family/',  // URL for Django view handling
            data: {csv_id: csv_id},
        
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
    
    