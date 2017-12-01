$(document).ready(function() {
	$('#navicon').on('click', function() {
		$("nav").slideToggle("fast")
	});
});


$(window).on("resize", function() {
  if ($("#navicon").is(":hidden")) {
    $("nav").show();
  } else {
		$("nav").hide();
	}
});
