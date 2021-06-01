$(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#displayTable tfoot th').each(function () {
        //var title = $(this).text();
        $(this).html('<input type="text" placeholder="Search" />');
    });

    var filesTable = $('#displayTable').DataTable({
        fixedHeader: true,
        lengthMenu: [[5, 10, 20, 50, 100, -1], [5, 10, 20, 50, 100, "All"]],
        pageLength: 50,
        dom: 'Bfrtip',
        order: [[1, "desc"]],
        columnDefs: [
            {
                "targets": [0],
                "visible": false,
                "searchable": false
            }
        ],
        buttons: ['pageLength', 'copy', 'excel', 'pdf', 'csv', 'print']
    });

    var r = $('#displayTable tfoot tr');
    r.find('th').each(function () {
        $(this).css('padding', '3px');
    });
    $('#displayTable thead').append(r);
    // Apply the filter
    // https://www.jqueryscript.net/demo/DataTables-Jquery-Table-Plugin/examples/api/multi_filter.html
    $("#displayTable thead input").on('keyup change', function () {
        filesTable
            .column($(this).parent().index() + ':visible')
            .search(this.value)
            .draw();
    });
    
    // // setup double click to redirect to edit page
    // $('#displayTable tbody').on('dblclick', 'tr', function () {
    // // get the row data from table
    // var data = filesTable.row(this).data();
    // // Simulate a mouse click:
    // window.location.href = editCodeBaseUrl_g + data[0];
    // });
});