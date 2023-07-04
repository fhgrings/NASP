BASE_URL = "http://localhost:5000"
function allocNSSI(id) {
  console.log("Testing"+id)
    alert("Creating a New Slice... S-NSSAI SD: 1 SST: 274401")
    var settings = {
        "url": "http://localhost:5000/nasp/allocNsi",
        "method": "PUT",
        "timeout": 0,
        "headers": {
          "Content-Type": "application/json"
        },
        "data": JSON.stringify({
          "NstTemplateId": String(id)
      }),
      };
      
      $.ajax(settings).done(function (response) {
        console.log(response);
        window.location.href = '/';
      });
    return ""
}
$('#myModal').on('shown.bs.modal', function () {
  alert("Testing")
  $('#myInput').trigger('focus')
})

function createNSST(form) {
  let formData = new FormData(form);
  var object = {};
  formData.forEach((value, key) => object[key] = value);
  var json = JSON.stringify(object);
  if (object.domain == "RAN") {
    URI = "/nssmfRAN/nsst"
  }
  if (object.domain == "Core") {
    URI = "/nssmfCore/nsst"
  }

  var settings = {
    "url": BASE_URL+URI,
    "method": "PUT",
    "timeout": 0,
    "headers": {
      "Content-Type": "application/json"
    },
    "data": json,
  };
  console.log(settings)

  $.ajax(settings).done(function (response) {
    console.log(response);
    window.location.href = 'nsst';
  });
}

function createNST(form) {
  URI = "/nasp/nst"
  let formData = new FormData(form);
  var object = {};
  formData.forEach((value, key) => object[key] = value);
  var json = JSON.stringify(object);
  var settings = {
    "url": BASE_URL+URI,
    "method": "PUT",
    "timeout": 0,
    "headers": {
      "Content-Type": "application/json"
    },
    "data": json,
  };
  console.log(settings)

  $.ajax(settings).done(function (response) {
    console.log(response);
    window.location.href = '/';
  });
}