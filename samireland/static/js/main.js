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

/*
$("#blog-nav").hover(function() {
	console.log("Hover!");
	$("nav").append($("<div>", {id: "year-links"}));
	var years = $("#blog-nav").attr("data-years").split(",");
	$.each(years, function(index, value) {

		$("#year-links").append("<div class='blog-year'>" + value + "</div>");
	});
}, function() {
	console.log("Unhover :(");
});
*/
