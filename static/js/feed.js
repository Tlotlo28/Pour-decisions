document.addEventListener("DOMContentLoaded", function () {
  var items = document.querySelectorAll("[data-reveal]");

  // Fallback for ancient browsers: just show everything.
  if (!("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("revealed"); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("revealed");
        observer.unobserve(entry.target);  // reveal once, then stop watching
      }
    });
  }, { threshold: 0.12 });

  items.forEach(function (el, i) {
    el.style.transitionDelay = (i % 6) * 0.06 + "s";  // gentle cascade per row
    observer.observe(el);
  });
});