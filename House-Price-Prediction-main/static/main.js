$(document).ready(function(){
    $("#submit").on("click", function(e){
        e.preventDefault();
        console.log("Estimate price button clicked");
        var sqft = document.getElementById("area");
        var bhk = $('#bhk').find(":selected").val();
        var bathrooms = $('#bath').find(":selected").val();
        var location = document.getElementById("location");
        console.log(sqft, bhk, bathrooms, location);
        // var estPrice = document.getElementById("uiEstimatedPrice");
        var flag1 = 0;
        var flag2 = 0;
        var flag3 = 0;

        if(sqft.value == "")
        {
          $(".errorSqft").text("*Above field is mandatory to fill up.");
          console.log($(".errorSqft"));
          flag1 = 1;
        }
        else if(parseInt(sqft.value) < 650){
          $(".errorSqft").text("*Given input is too low. Minimum square feet is required 650 sqft.");
          flag1 = 1;
        }else{
          $(".errorSqft").text("");
          flag1 = 0;
        }
        
        if(bhk == 0){
          $(".errorBhk").text("*Kindly select any one option.");
          flag2 = 1;
        }else{
          $(".errorBhk").text("");
          flag2 = 0;
        }
        
        if(bathrooms == 0){
          $(".errorBath").text("*Kindly select any one option.");
          flag3 = 1;
        }else{
          $(".errorBath").text("");
          flag3 = 0;
        }

        if(flag1 == 0 && flag2 == 0 && flag3 == 0){
          var url = "http://127.0.0.1:5000/predict_home_price"; 
        
          $.post(url, {
              total_sqft: parseFloat(sqft.value),
              bhk: parseInt(bhk),
              bath: parseInt(bathrooms),
              location: location.value
          },function(data, status) {
              console.log(data.estimated_price);
              $modal = $("#exampleModalCenter");
              $modal.modal("show");
              $("#predicted_price").text(data.estimated_price.toString());
              console.log(status);
          });
        }

    })

      var url = "http://127.0.0.1:5000/get_location_names"; 
      $.get(url, function (data, status) {
        console.log("got response for get_location_names request");
        if (data) {
            console.log("got it");
          var locations = data.locations;
          $("#location").empty();
          console.log($("#location"));
          for (var i in locations) {
            var opt = new Option(locations[i]);
            $("#location").append(opt);
          }
        }
      });

      $("#submitRegister").on("click", function(e){
        console.log("clicked");  
        e.preventDefault();

        username1 = $("#username").val();
        email1 = $("#email").val();
        password1 = $("#password").val();
        var url = "http://127.0.0.1:5000/python_register"; 
        
          $.post(url, {
              username: username1,
              email: email1,
              password: password1
          },function(data, status) {
              console.log(data);
              window.location.href = "/";
              console.log(status);
          });
      });

      
});

