var runner;
var answer;
var canvas;
var context;

// Resize canvas when page loads
$(window).load(function() {
  canvas = document.getElementsByTagName("canvas")[0];
  canvas.width  = $("main").width() * 0.9;
})


// For a given tone, decide which staff to use
function pickCleff(note) {
  var cleff;
  if ((note[1] > 4) || ((note[1] === 4) && (["G", "A", "B"].indexOf(note[0].slice(0, 1)) != -1))) {
    cleff = "treble";
  } else if ((note[1] < 3) || ((note[1] === 3) && (["C", "D", "E", "F"].indexOf(note[0].slice(0, 1)) != -1))) {
    cleff = "bass";
  } else {
    cleff = ["treble", "bass"][Math.floor(Math.random() * 2)];
  }
  return cleff;
}


// Converts a note to its vexflow equivalent
function processNote(note) {
  if (note.length == 1) {
    return note;
  } else {
    return note.slice(0, 1) + {"♯": "#", "♭": "b"}[note.slice(1)];
  }
}


// Paint a staff with an optional note
function paintGrandStaff(note) {
  var renderer = new Vex.Flow.Renderer(canvas, Vex.Flow.Renderer.Backends.CANVAS);
  context = renderer.getContext();
  context.clearRect(0, 0, canvas.width, canvas.height);
  var topStaff = new Vex.Flow.Stave(10, 0, canvas.width - 20, {spacing_between_lines_px: 10});
  var bottomStaff = new Vex.Flow.Stave(10, 100, canvas.width - 20, {spacing_between_lines_px: 10});
  topStaff.addClef('treble').setContext(context).draw();
  bottomStaff.addClef('bass').setContext(context).draw();
  $("canvas").attr("staff", "yes");
  if (note != null) {
    var allocatedCleff = pickCleff(note);
    var voice = new Vex.Flow.Voice({
      num_beats: 1,
      beat_value: 4,
      resolution: Vex.Flow.RESOLUTION
    });
    var staveNotes;
    if (note[0].length == 1) {
      staveNotes = [new Vex.Flow.StaveNote(
       { clef: allocatedCleff, keys: [processNote(note[0]) + "/" + note[1]], duration: "q" }
      )];
    } else {
      staveNotes = [new Vex.Flow.StaveNote(
       { clef: allocatedCleff, keys: [processNote(note[0]) + "/" + note[1]], duration: "q" }
      ).addAccidental(0, new Vex.Flow.Accidental(processNote(note[0]).slice(1)))];
    }
    voice.addTickables(staveNotes);
    var formatter = new Vex.Flow.Formatter().joinVoices([voice]).format([voice], 500);
    voice.draw(context,allocatedCleff === "treble" ? topStaff : bottomStaff);
    //voice.draw(context, bottomStaff);
  }
}


// Prep the canvas when option changed
$("input[type=button]").on("click", function() {
  $(this).addClass("pure-button-active");
  $("input[type=button]").not(this).removeClass("pure-button-active");
  if ($("#stop").hasClass("pure-button-disabled")) {
    if ($("#id_sheets").hasClass("pure-button-active")) {
      paintGrandStaff(null);
    } else {
      context = canvas.getContext("2d");
      context.clearRect(0, 0, canvas.width, canvas.height);
      $("canvas").attr("staff", "no");
    }
  }
})


// Start the practice
$("#start").on("click", function() {
  if ($("#stop").hasClass("pure-button-disabled")) {
    $('#start').addClass("pure-button-disabled");
    $('#stop').removeClass("pure-button-disabled");

    var seconds = $("#id_seconds").val();
    if ($.isNumeric(seconds)) {
      seconds = parseFloat(seconds);
    } else {
      seconds = 2.0;
    }

    var notes = ["A", "B", "C", "D", "E", "F", "G"];
    if ($("#id_black").is(":checked")) {
      notes = notes.concat(["A♭", "A♯", "B♭", "C♯", "D♭", "D♯", "E♭", "F♯", "G♭", "G♯"])
    }
    if ($("#id_chords").hasClass("pure-button-active")) {
      chords = [];
      for (var i = 0; i < notes.length; i++) {
        chords.push(notes[i] + " Major")
      }
      notes = chords;
    } else if ($("#id_sheets").hasClass("pure-button-active")) {
      var keys = [2, 3, 4, 5];
      tones = [];
      for (var n = 0; n < notes.length; n++) {
        for (var k = 0; k < keys.length; k++) {
          tones.push([notes[n], keys[k]])
        }
      }
      notes = tones;
    }

    if ($("#id_sheets").hasClass("pure-button-active")) {
      var note = notes[Math.floor(Math.random() * notes.length)];
      paintGrandStaff(note);
      $("canvas").attr("display", note);
      window.setTimeout(function() {
       context.font = "40px Arial";
       context.textAlign = "center";
       context.textBaseline = "middle";
       context.fillText(note[0], canvas.width / 2, canvas.height / 2);
      }, seconds * 800);
      runner = window.setInterval(function(){
        next_notes = notes.slice(0);
        next_notes.splice(next_notes.indexOf(note), 1);
        note = next_notes[Math.floor(Math.random() * next_notes.length)]
        paintGrandStaff(note);
        $("canvas").attr("display", note);
        answer = window.setTimeout(function() {
         context.font = "40px Arial";
         context.textAlign = "center";
         context.textBaseline = "middle";
         context.fillText(note[0], canvas.width / 2, canvas.height / 2);
        }, seconds * 800);
      }, seconds * 1000);
    } else {
      context = canvas.getContext("2d");
      var note = notes[Math.floor(Math.random() * notes.length)];
      context.font = $("#id_notes").hasClass("pure-button-active") ? "120px Arial" : "60px Arial";
      context.textAlign = "center";
      context.textBaseline = "middle";
      context.fillText(note, canvas.width / 2, canvas.height / 2);
      $("canvas").attr("display", note);
      runner = window.setInterval(function(){
        next_notes = notes.slice(0);
        next_notes.splice(next_notes.indexOf(note), 1);
        context.clearRect(0, 0, canvas.width, canvas.height);
        note = next_notes[Math.floor(Math.random() * next_notes.length)]
        context.fillText(note, canvas.width / 2, canvas.height / 2);
        $("canvas").attr("display", note);
      }, seconds * 1000);
    }
  }
})


// Stop the practice
$("#stop").on("click", function() {
  $('#stop').addClass("pure-button-disabled");
  $('#start').removeClass("pure-button-disabled");

  clearInterval(runner);
  clearInterval(answer);
  context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
  $("canvas").attr("staff", "no");
  $("canvas").attr("display", "");
  if ($("#id_sheets").hasClass("pure-button-active")) {
    paintGrandStaff(null);
  }
})
