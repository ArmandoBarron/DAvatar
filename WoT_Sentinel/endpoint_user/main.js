//Código para Datables

//$('#example').DataTable(); //Para inicializar datatables de la manera más simple

$(document).ready(function() {    
    $('#example').DataTable({
    //para cambiar el lenguaje a español
        "language": {
                "lengthMenu": "Show _MENU_ records",
                "zeroRecords": "No results found",
                "info": "Showing records from _START_ to _END_ out of a total of _TOTAL_ records",
                "infoEmpty": "Showing records from 0 to 0 out of a total of 0 records",
                "infoFiltered": "(filtering a total of _MAX_ records)",
                "sSearch": "Search:",
                "oPaginate": {
                    "sFirst": "First",
                    "sLast":"Last",
                    "sNext":"Next",
                    "sPrevious": "Previous"
			     },
			     "sProcessing":"Processing...",
            }
    });     
});