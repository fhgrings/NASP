BASE_URL = "http://localhost:5000"
function allocNSI(nst) {
  alert("Test")
  console.log(nst)
  alert("Creating a New Slice...")
  // request("PUT", "http://165.232.128.22:5000/nasp/nsi", JSON.stringify(nst))
  // var settings = {
  //     "url": "http://localhost:5000/nasp/allocNsi",
  //     "method": "PUT",
  //     "timeout": 0,
  //     "headers": {
  //       "Content-Type": "application/json"
  //     },
  //     "data": JSON.stringify({
  //       "NstTemplateId": String(id)
  //   }),
  //   };
    
  //   $.ajax(settings).done(function (response) {
  //     console.log(response);
  //     window.location.href = '/';
  //   });
  // return ""
}
$('#myModal').on('shown.bs.modal', function () {
  alert("Testing")
  $('#myInput').trigger('focus')
})

function addAMF_temp(form){
  let formData = new FormData(form);
  var object = {};
  console.log(formData)
  formData.forEach((value, key) => object[key] = value);
  var json = JSON.stringify(object);

  var settings = {
    "url": "http://165.232.128.22:5000/nssmfCore/nsst",
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

function createNSST(form) {
  let formData = new FormData(form);
  var object = {};
  formData.forEach((value, key) => object[key] = value);
  var json = JSON.stringify(object);
  console.log(object)
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

function createSliceGSMA(form) {
  let formData = new FormData(form)
  var object = {};
  formData.forEach((value, key) => object[key] = value);
  var json = JSON.stringify(object);
  var data = JSON.parse(json)
  data.description = JSON.parse(data.description)
  console.log(data)
  console.log(JSON.stringify(data))
  request("PUT", "http://165.232.128.22:5000/nasp/nsi", JSON.stringify(data))
}

function request(method,url,data) {
  var settings = {
    "url": url,
    "method": method,
    "timeout": 0,
    "headers": {
      "Content-Type": "application/json"
    },
    "data": data,
  };
  console.log(settings)

  $.ajax(settings).done(function (response) {
    console.log(response);
    window.location.href = '/';
  });
}