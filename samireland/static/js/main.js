$(document).ready(function() {
	$('#navicon').on('click', function() {
		$("nav").slideToggle("fast");
        $("header").css("box-shadow", null);
	});
});


$(window).on("resize", function() {
  if ($("#navicon").is(":hidden")) {
    $("nav").show();
  } else {
		$("nav").hide();
	}
});


function clickCard(url) {
    if (event.target.nodeName != "A") {
        window.location.href = url;
    }
}
