$(function() {
  $(".auto_submit_field").change(function() {
   	$(this).parents(".auto_submit_form").submit();
  });
});