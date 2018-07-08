$(document).ready(function() {
  let project = $('input[name="project"]').val();

  $('.add_video').click(function() {
    $('.videos').append('<input type="file" name="video">')
    return false
  });

  $('.add_photo').click(function() {
    $('.photos').append('<input type="file" name="photo">')
    return false
  });

});
