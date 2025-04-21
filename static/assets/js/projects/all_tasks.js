$(document).ready(function() {
    var table = $('#tasksTable').DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.25/i18n/Vietnamese.json"
        },
        "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
               "<'row'<'col-sm-12'tr>>" +
               "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        "columnDefs": [
            { "orderable": false, "targets": [4, 5] } 
        ],
        "initComplete": function() {
            $('#tasksTable_wrapper').addClass('loaded');
        }
    });

    $('#projectFilter').change(function() {
        table.column(1).search($(this).val()).draw();
    });

    $('#statusFilter').change(function() {
        table.column(3).search($(this).val()).draw();
    });

    $('#resetFilter').click(function() {
        $('#projectFilter, #statusFilter').val('').trigger('change');
        table.search('').columns().search('').draw();
    });

    $('[data-bs-toggle="tooltip"]').tooltip();
});