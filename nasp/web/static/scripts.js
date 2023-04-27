function allocNSSI() {
    alert("Creating a New Slice...")
    var settings = {
        "url": "http://localhost:5000/nasp/allocNsi",
        "method": "PUT",
        "timeout": 0,
        "headers": {
          "Content-Type": "application/json"
        },
        "data": JSON.stringify({
          "NsiTemplateId": "1"
      }),
      };
      
      $.ajax(settings).done(function (response) {
        console.log(response);
        window.location.href = 'table';
      });
    return ""
}
$('#myModal').on('shown.bs.modal', function () {
  alert("Testing")
  $('#myInput').trigger('focus')
})