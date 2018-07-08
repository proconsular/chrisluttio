$(document).ready(function() {
  var num = 0;

  $('.add_photo').click(function() {
    $('.photos').append('<input type="file" name="photo">')
    return false
  })

});
