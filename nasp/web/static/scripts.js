function allocNSSI() {
    alert("Creating a New Slice...")
    var settings = {
        "url": "http://localhost:5000//allocNssmfCore",
        "method": "PUT",
        "timeout": 0,
        "headers": {
          "Content-Type": "application/json"
        },
        "data": JSON.stringify({
          "NSSAI": {
            "sst": "1",
            "sd": "24401"
          }
        }),
      };
      
      $.ajax(settings).done(function (response) {
        console.log(response);
        window.location.href = 'table';
      });
    return ""
}