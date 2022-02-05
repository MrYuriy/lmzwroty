$("#next").click(function () {
    var nrorder = $('#nrorder').val();
    var sku = $('#sku').val();
    var quantity = $('#quantity').val();
    var quantity_not_damaget = $("#quantity_not_damaget").val();
    $.ajax({
        url: 'ajax/add-product-to-order' ,
        data: {
          'nrorder': nrorder,
          'sku': sku,
          'quantity': quantity,
          'quantity_not_damaget':quantity_not_damaget,
        },
        dataType: 'json',
        success: function (data) {
          // $("#next").prop("disabled", false);
        }
      });
    });