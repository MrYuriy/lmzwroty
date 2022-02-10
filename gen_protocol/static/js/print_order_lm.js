$("#download").click(function () {
    var nrorder = $('#nrorder').val();
    
    $.ajax({
        url: 'generate-pdf-lm' ,
        data: {
          'nrorder': nrorder,
        },
        dataType: 'json',
        success: function (data) {
          // $("#continue").prop("disabled", false);
        }
      });
    });