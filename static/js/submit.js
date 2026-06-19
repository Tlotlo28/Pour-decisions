document.addEventListener("DOMContentLoaded", function () {
  setupMeters();
  setupCompanions();
  setupDrinks();
});

/* ---- Officer's assessment meters ---- */
function meterColor(value) {
  if (value <= 3) return "#3f7d4f";   // green - mild
  if (value <= 6) return "#c9a227";   // amber - concerning
  if (value <= 8) return "#cf6a1f";   // orange - serious
  return "#8b1a1a";                   // red - legendary
}

function setupMeters() {
  document.querySelectorAll(".meter input[type='range']").forEach(function (slider) {
    var readout = document.querySelector('.meter-val[data-for="' + slider.id + '"]');
    var min = Number(slider.min || 0);
    var max = Number(slider.max || 100);

    function paint() {
      var value = Number(slider.value);
      var pct = ((value - min) / (max - min)) * 100;
      var color = meterColor(value);
      slider.style.background =
        "linear-gradient(to right, " + color + " 0%, " + color + " " + pct +
        "%, var(--line) " + pct + "%, var(--line) 100%)";
      if (readout) {
        readout.textContent = value;
        readout.style.color = color;
        readout.classList.add("bump");
        setTimeout(function () { readout.classList.remove("bump"); }, 120);
      }
    }
    slider.addEventListener("input", paint);
    paint();
  });
}

/* ---- "Alone" locks out the other companions ---- */
function setupCompanions() {
  var wrapper = document.querySelector(".companions");
  if (!wrapper) return;

  var exclusiveValues = (wrapper.getAttribute("data-exclusive") || "")
    .split(",").filter(Boolean);
  var boxes = wrapper.querySelectorAll('input[type="checkbox"]');

  var exclusiveBoxes = [];
  var normalBoxes = [];
  boxes.forEach(function (box) {
    if (exclusiveValues.indexOf(box.value) !== -1) exclusiveBoxes.push(box);
    else normalBoxes.push(box);
  });

  function apply() {
    var locked = exclusiveBoxes.some(function (b) { return b.checked; });
    normalBoxes.forEach(function (b) {
      if (locked) b.checked = false;
      b.disabled = locked;
      var lbl = b.closest("label");
      if (lbl) lbl.classList.toggle("is-disabled", locked);
    });
  }

  boxes.forEach(function (box) { box.addEventListener("change", apply); });
  apply();
}

/* ---- Add / remove drink rows + "can't remember" toggle ---- */
function setupDrinks() {
  var list = document.getElementById("drink-list");
  var addBtn = document.getElementById("drink-add");
  if (!list || !addBtn) return;

  function newRow() {
    var row = document.createElement("div");
    row.className = "drink-row";
    row.innerHTML =
      '<input type="text" name="drink" placeholder="e.g. Tequila" maxlength="80">' +
      '<button type="button" class="drink-remove">Remove</button>';
    return row;
  }

  addBtn.addEventListener("click", function () {
    var row = newRow();
    list.appendChild(row);
    row.querySelector("input").focus();
  });

  // Event delegation: one listener handles remove on current AND future rows.
  list.addEventListener("click", function (e) {
    if (e.target.classList.contains("drink-remove")) {
      e.target.closest(".drink-row").remove();
    }
  });

  var forgot = document.getElementById("id_drinks_forgotten");
  if (forgot) {
    function toggle() {
      var off = forgot.checked;
      list.querySelectorAll("input[name='drink']").forEach(function (i) {
        i.disabled = off;
      });
      addBtn.disabled = off;
      list.classList.toggle("is-disabled", off);
    }
    forgot.addEventListener("change", toggle);
    toggle();
  }
}