document.addEventListener("DOMContentLoaded", function () {
  // --- Scroll-reveal cards ---
  var items = document.querySelectorAll("[data-reveal]");
  if (!("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("revealed"); });
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el, i) {
      el.style.transitionDelay = (i % 6) * 0.06 + "s";
      observer.observe(el);
    });
  }

  // --- "The night's still young" scroll cue ---
  var cue = document.getElementById("scrollCue");
  if (cue) {
    function updateCue() {
      var scrollable = document.documentElement.scrollHeight - window.innerHeight;
      var nearBottom = window.scrollY > scrollable - 120;
      if (scrollable > 200 && !nearBottom) {
        cue.classList.add("show");
      } else {
        cue.classList.remove("show");
      }
    }
    cue.addEventListener("click", function () {
      window.scrollBy({ top: window.innerHeight * 0.85, behavior: "smooth" });
    });
    window.addEventListener("scroll", updateCue, { passive: true });
    window.addEventListener("resize", updateCue);
    updateCue();
  }
});