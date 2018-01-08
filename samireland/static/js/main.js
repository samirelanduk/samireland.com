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


function editText(button, csrf) {
    var paragraphs = $(button).parent().find("p");
    paragraphs.each(function(index, p) {
        p.remove();
    })
    button.remove();
    var form = $(".hidden-form");
    form.show();
}
