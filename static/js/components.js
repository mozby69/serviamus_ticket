$(document).ready(function() {
    var rowsPerPage = 5; // Number of rows per page
    var totalRows = $("#myTable tr").length;
    var totalPages = Math.ceil(totalRows / rowsPerPage);
    var currentPage = 1;
    var pageNumbersToShow = 5; // Number of page numbers to display at a time

    function showPage(page) {
        $("#myTable tr").hide();
        $("#myTable tr").slice((page - 1) * rowsPerPage, page * rowsPerPage).show();
        updatePageNumbers();
        updatePaginationControls();
    }

    function updatePaginationControls() {
        $("#prev").prop("disabled", currentPage === 1);
        $("#next").prop("disabled", currentPage === totalPages);
    }

    function updatePageNumbers() {
        var pageNumbersHtml = '';

        // Add first and previous controls
        pageNumbersHtml += '<button id="first">«</button> ';
        pageNumbersHtml += '<button id="prev">‹</button> ';

        // Calculate start and end page numbers
        var startPage = Math.max(1, currentPage - Math.floor(pageNumbersToShow / 2));
        var endPage = Math.min(totalPages, startPage + pageNumbersToShow - 1);

        if (endPage - startPage + 1 < pageNumbersToShow) {
            startPage = Math.max(1, endPage - pageNumbersToShow + 1);
        }

        if (startPage > 1) {
            pageNumbersHtml += '<button class="page-number" data-page="1">1</button> ';
            if (startPage > 2) {
                pageNumbersHtml += '... ';
            }
        }

        for (var i = startPage; i <= endPage; i++) {
            pageNumbersHtml += '<button class="page-number" data-page="' + i + '">' + i + '</button> ';
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                pageNumbersHtml += '... ';
            }
            pageNumbersHtml += '<button class="page-number" data-page="' + totalPages + '">' + totalPages + '</button> ';
        }

        // Add next and last controls
        pageNumbersHtml += '<button id="next">›</button> ';
        pageNumbersHtml += '<button id="last">»</button>';

        $("#page-numbers").html(pageNumbersHtml);
        $(".page-number").removeClass('active');
        $(".page-number[data-page='" + currentPage + "']").addClass('active');
    }

    $("#page-numbers").on("click", ".page-number", function() {
        var page = $(this).data("page");
        currentPage = page;
        showPage(currentPage);
    });

    $("#page-numbers").on("click", "#first", function() {
        currentPage = 1;
        showPage(currentPage);
    });

    $("#page-numbers").on("click", "#last", function() {
        currentPage = totalPages;
        showPage(currentPage);
    });

    $("#page-numbers").on("click", "#prev", function() {
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
        }
    });

    $("#page-numbers").on("click", "#next", function() {
        if (currentPage < totalPages) {
            currentPage++;
            showPage(currentPage);
        }
    });

    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        if (value === "") {
            // Reload initial data
            currentPage = 1;
            showPage(currentPage); // Display first 5 rows
        } else {
            $("#myTable tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
            });
        }
    });

    // Initial page setup
    showPage(currentPage);
});
