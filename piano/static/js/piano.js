var runner;

$("#start").on("click", function() {
  $('#start').attr("disabled", true);
  $('#stop').attr("disabled", false);
  var seconds = $("#id_seconds").val();
  if ($.isNumeric(seconds)) {
    seconds = parseFloat(seconds);
  } else {
    seconds = 5.0;
  }
  var notes = [
       "A", "B", "C", "D", "E", "F", "G",
       "A♭", "A♯", "B♭", "C♯", "D♭", "D♯", "E♭", "F♯", "G♭", "G♯"
      ]
  $("#display").html(notes[Math.floor(Math.random() * notes.length)]);
  runner = window.setInterval(function(){
    next_notes = notes.slice(0);
    next_notes.splice(next_notes.indexOf($("#display").html()), 1);
    $("#display").html(next_notes[Math.floor(Math.random() * next_notes.length)]);
  }, seconds * 1000);
})


$("#stop").on("click", function() {
  $('#start').attr("disabled", false);
  $('#stop').attr("disabled", true);
  clearInterval(runner);
  $("#display").html("");
})
