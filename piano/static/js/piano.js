var runner;
var canvas;
var context;

// Resize canvas when page loads
$(window).load(function() {
  canvas = document.getElementsByTagName("canvas")[0];
  canvas.width  = $("main").width() * 0.9;
})


// Prep the canvas when option changed
$("input[name=options]").on("click", function() {
  if ($("#stop").is(":disabled")) {
    if ($("#id_sheets").is(':checked')) {
      var renderer = new Vex.Flow.Renderer(canvas, Vex.Flow.Renderer.Backends.CANVAS);
      context = renderer.getContext();
      var topStaff = new Vex.Flow.Stave(10, -50, canvas.width - 20, {spacing_between_lines_px: 15});
      var bottomStaff = new Vex.Flow.Stave(10, 50, canvas.width - 20, {spacing_between_lines_px: 15});
      topStaff.addClef('treble').setContext(context).draw();
      bottomStaff.addClef('bass').setContext(context).draw();
    } else {
      context = canvas.getContext("2d");
      context.clearRect(0, 0, canvas.width, canvas.height);
    }
  }
})


// Start the practice
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
    
  } else {
    context = canvas.getContext("2d");
    var note = notes[Math.floor(Math.random() * notes.length)];
    context.font = "60px Arial";
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.fillText(note, canvas.width / 2, canvas.height / 2);
    runner = window.setInterval(function(){
      next_notes = notes.slice(0);
      next_notes.splice(next_notes.indexOf(note), 1);
      context.clearRect(0, 0, canvas.width, canvas.height);
      note = next_notes[Math.floor(Math.random() * next_notes.length)]
      context.fillText(note, canvas.width / 2, canvas.height / 2);
    }, seconds * 1000);
  }
})


// Stop the practice
$("#stop").on("click", function() {
  $('#start').attr("disabled", false);
  $('#stop').attr("disabled", true);

  clearInterval(runner);
  context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
})
