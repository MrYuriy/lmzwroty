$("#save").click(function () {
    var user = $('#user').val();
    var from_location = $('#from_location').val();
    var to_location = $('#to_location').val();
    var inventory_adres = $('#inventory_adres').val();
    var inventory_qty = $('#inventory_qty')().val;
    var from_location_arc = $('#from_location_arc').val();
    var to_location_arc = $('#to_location_arc').val();
    $.ajax({
        url: 'ajax/save-user' ,
        data: {
            'user': user,
            'from_location': from_location,
            'to_location': to_location,
            'inventory_adres': inventory_adres,
            'inventory_qty':inventory_qty,
            'from_location_arc':from_location_arc,
            'to_location_arc':to_location_arc
        },
        dataType: 'json',
        success: function (data) {
          // $("#next").prop("disabled", false);
        }
      });
    });


