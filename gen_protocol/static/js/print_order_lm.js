$("#download").click(function () {
    var nrorder = $('#nrorder').val();
    
    $.ajax({
        url: 'gen_pdf' ,
        data: {
          'nrorder': nrorder,
        },
        dataType: 'json',
        success: function (data) {
          // $("#continue").prop("disabled", false);
        }
      });
    });