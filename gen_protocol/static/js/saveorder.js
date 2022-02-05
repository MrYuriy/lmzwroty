$("#continue").click(function () {
    var nrorder = $('#nrorder').val();
    var tapydelivery = $('#tapydelivery').find('option:selected').val();
    $.ajax({
        url: 'ajax/saveorder',
        data: {
          'nrorder': nrorder,
          'tapydelivery': tapydelivery,
        },
        dataType: 'json',
        success: function (data) {
          // $("#continue").prop("disabled", false);
        }
      });
    });