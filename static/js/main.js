$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();


function displayResult(data) {
  // display the result
  // imageDisplay.classList.remove("loading");
  hide(loader);
  predResult.innerHTML = data.result;
  show(predResult);
}
    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });
function clearImage() {
  $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
}
    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            dataType: 'html',
            cache: false,
            processData: false,
            async: true,
            success: function (response) {
                // Get and display the result
                
              if(response.prediction == "no_crack"){
                
                alert(response);
                
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').html(' FIRST TEST RESULT : '+ response.prediction  +'<br>'+'<br>'+' Sending for second test.....'+'<br>'+'<br>'+' SECOND TEST RESULT :' + response.prediction1  );
                //  $('#result').text('');
                        $('.image-section').show();

                }else{
                
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result: '+ response.prediction);
                
                }
               
                
                 $('.loader').hide();
               //var one =  $(".img-preview").html();
             
               //$("#image-source").show();
            //  $("#image-source").    (one);
                
                
            },
        });
    });

});
