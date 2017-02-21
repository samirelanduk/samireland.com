$('#navicon').on('click', function() {
	$("nav").slideToggle()
});

$(window).on("resize", function() {
  if ($("#navicon").is(":hidden")) {
    $("nav").show();
  } else {
		$("nav").hide();
	}
});
