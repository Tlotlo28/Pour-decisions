document.addEventListener("DOMContentLoaded", function () {
  var box = document.querySelector(".breathalyzer");
  if (!box) return;

  var slider = box.querySelector(".breath-slider");
  var needle = box.querySelector(".gauge-needle");
  var avgNeedle = box.querySelector(".gauge-avg");
  var scoreEl = box.querySelector(".breath-score");
  var zoneEl = box.querySelector(".breath-zone");
  var submitBtn = box.querySelector(".breath-submit");
  var consensus = box.querySelector(".breath-consensus");

  var rateUrl = box.dataset.rateUrl;
  var csrftoken = box.dataset.csrf;

  function zoneFor(v) {
    if (v <= 20) return "Tipsy";
    if (v <= 40) return "Buzzed";
    if (v <= 60) return "Sloshed";
    if (v <= 80) return "Blackout";
    return "Legendary";
  }
  function colorFor(v) {
    if (v <= 20) return "#3f7d4f";
    if (v <= 40) return "#c9a227";
    if (v <= 60) return "#cf6a1f";
    if (v <= 80) return "#b23a1a";
    return "#8b1a1a";
  }
  function angleFor(v) { return -90 + ((v - 1) / 99) * 180; }

  function renderNeedle(v) {
    needle.style.transform = "rotate(" + angleFor(v) + "deg)";
    scoreEl.textContent = v;
    scoreEl.style.color = colorFor(v);
    zoneEl.textContent = zoneFor(v);
  }

  function showAverage(avg, count) {
    if (!avg) return;
    avgNeedle.style.transform = "rotate(" + angleFor(avg) + "deg)";
    avgNeedle.classList.add("show");
    consensus.hidden = false;
    consensus.textContent = "Street consensus: " + avg + " - " + zoneFor(avg) +
      ", from " + count + " reading" + (count === 1 ? "" : "s") + ".";
  }

  slider.addEventListener("input", function () {
    renderNeedle(Number(slider.value));
  });

  var mine = Number(box.dataset.mine);
  if (mine) { slider.value = mine; submitBtn.textContent = "Update my reading"; }
  renderNeedle(Number(slider.value));
  showAverage(Number(box.dataset.average), Number(box.dataset.count));

  submitBtn.addEventListener("click", function () {
    submitBtn.disabled = true;
    fetch(rateUrl, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: "score=" + encodeURIComponent(slider.value),
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.ok) {
          showAverage(data.average, data.count);
          submitBtn.textContent = "Update my reading";
        }
        submitBtn.disabled = false;
      })
      .catch(function () { submitBtn.disabled = false; });
  });
});