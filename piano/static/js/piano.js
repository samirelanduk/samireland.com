var runner;

$("#start").on("click", function() {
  $('#start').attr("disabled", true);
  $('#stop').attr("disabled", false);

  var seconds = $("#id_seconds").val();
  if ($.isNumeric(seconds)) {
    seconds = parseFloat(seconds);
  } else {
    seconds = 2.0;
  }

  var notes;
  if ($("#id_chords").is(':checked')) {
    notes = [
     "A Major", "B Major", "C Major", "D Major", "E Major", "F Major", "G Major"
    ]
  } else if ($("#id_sheets").is(':checked')) {
    notes = [
     0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5
    ]
  } else {
    notes = [
     "A", "B", "C", "D", "E", "F", "G",
     "A♭", "A♯", "B♭", "C♯", "D♭", "D♯", "E♭", "F♯", "G♭", "G♯"
    ]
  }

  if ($("#id_sheets").is(':checked')) {
    /*var position = notes[Math.floor(Math.random() * notes.length)];
    $("#display").find("svg").append(
     "<ellipse id='note' cx='180' cy='" +
     ((position * 20) + 10) +
    "' data='" +
     position +
     "' rx='10' ry='8' stroke='black' stroke-width='3' fill='black' />"
    )
    $("#display").html($("#display").html());
    runner = window.setInterval(function(){
      next_notes = notes.slice(0);
      next_notes.splice(next_notes.indexOf($("#note").attr("data")), 1);
      position = next_notes[Math.floor(Math.random() * next_notes.length)];
      $("#note").attr("y", (position * 20) + 10);
      $("#note").attr("data", (position - 10) / 20);
    }, seconds * 1000);*/
  } else {
    var canvas = document.getElementsByTagName("canvas")[0];
    var context = canvas.getContext("2d");
    var first_note = notes[Math.floor(Math.random() * notes.length)];
    context.font = "60px Arial";
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.fillText(first_note, canvas.width / 2, canvas.height / 2);
    runner = window.setInterval(function(){
      next_notes = notes.slice(0);
      next_notes.splice(next_notes.indexOf($("#display").html()), 1);
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.fillText(next_notes[Math.floor(Math.random() * next_notes.length)], canvas.width / 2, canvas.height / 2);
    }, seconds * 1000);
  }
})


$("#stop").on("click", function() {
  $('#start').attr("disabled", false);
  $('#stop').attr("disabled", true);

  clearInterval(runner);
  var canvas = document.getElementsByTagName("canvas")[0];
  var context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
})


$("input[name=options]").on("click", function() {
  if ($("#stop").is(":disabled")) {
    if ($("#id_sheets").is(':checked')) {
      $("#display").html($("#svgcontainer").html());
    } else {
      $("#display").html("");
    }
  }
})
