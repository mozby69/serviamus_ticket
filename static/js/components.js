$(document).ready(function () {
    var rowsPerPage = 5; // Number of rows per page
    var currentPage = 1;
    var pageNumbersToShow = 5; // Number of page numbers to display at a time

    function calculateTotalPages() {
        var totalRows = $("#myTable tr").length;
        return Math.ceil(totalRows / rowsPerPage);
    }

    function showPage(page) {
        var totalPages = calculateTotalPages(); // Calculate total pages dynamically
        $("#myTable tr").hide();
        $("#myTable tr").slice((page - 1) * rowsPerPage, page * rowsPerPage).show();
        updatePageNumbers(totalPages);
        updatePaginationControls(totalPages);
    }

    function updatePaginationControls(totalPages) {
        $("#prev").prop("disabled", currentPage === 1);
        $("#next").prop("disabled", currentPage === totalPages);
    }

    function updatePageNumbers(totalPages) {
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

    $("#page-numbers").on("click", ".page-number", function () {
        var page = $(this).data("page");
        currentPage = page;
        showPage(currentPage);
    });

    $("#page-numbers").on("click", "#first", function () {
        currentPage = 1;
        showPage(currentPage);
    });

    $("#page-numbers").on("click", "#last", function () {
        currentPage = calculateTotalPages(); // Calculate total pages dynamically
        showPage(currentPage);
    });

    $("#page-numbers").on("click", "#prev", function () {
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
        }
    });

    $("#page-numbers").on("click", "#next", function () {
        if (currentPage < calculateTotalPages()) { // Calculate total pages dynamically
            currentPage++;
            showPage(currentPage);
        }
    });

    $("#myInput").on("keyup", function () {
        var value = $(this).val().toLowerCase().trim();
        if (value === "") {
            // Reload initial data
            currentPage = 1;
            showPage(currentPage); // Display first 5 rows
        } else {
            $("#myTable tr").filter(function () {
                var rowText = $(this).text().toLowerCase().replace(/[\W_]/g, ''); // Remove special characters
                var searchText = value.replace(/[\W_]/g, ''); // Remove special characters from search term
                $(this).toggle(rowText.indexOf(searchText) > -1);
            });
        }
    });

    // Initial page setup
    showPage(currentPage);
});
