$("#sku").focusout(function () {
  var input = $('#sku').val();
  if (input != '') {
    $.ajax({
        url: 'ajax/get-response' ,
        data: {
          'sku': input
        },
        dataType: 'json',
        success: function (data) {
          document.getElementById('p-text').innerHTML = data["response"];
        }
      });
  }
  });