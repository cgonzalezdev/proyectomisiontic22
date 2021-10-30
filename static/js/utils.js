$("#clickModalPPD").click(function(){
  document.getElementById('modalPPD').classList.add('is-active');
});
$("#deleteModalPPD").click(function(){
  document.getElementById('modalPPD').classList.remove('is-active');
});

$('#imgUpload').change(function(e){
  var fileName = e.target.files[0].name;
  $('.file-name').css("visibility","visible");
  $(".file-name").text( fileName ); 
});

$("#clickModalListComentarios").click(function(){
  document.getElementById('modalListComentarios').classList.add('is-active');
});
$("#deletemodalListComentarios").click(function(){
  document.getElementById('modalListComentarios').classList.remove('is-active');
});