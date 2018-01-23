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
    var paragraphs = $(button).parent().find("p, figure, ol, ul");
    paragraphs.each(function(index, p) {
        p.remove();
    })
    button.remove();
    var form = $(".hidden-form");
    form.show();
}


function makeDeletionAppear(button) {
    var form = $(button).parent().find(".hidden-form")[0];
    console.log(form)
    $(form).show();
}


function hideDeletion(button) {
    var form = $(".hidden-form");
    form.hide();
}
