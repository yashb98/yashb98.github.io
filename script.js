(function () {
  var calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var chart = document.querySelector(".fp");

  // Every estimate starts on the zero line and moves out when the chart first
  // comes into view. Without this script the chart simply renders in place.
  if (chart && !calm && "IntersectionObserver" in window) {
    chart.querySelectorAll(".fp-row").forEach(function (row, index) {
      row.style.setProperty("--delay", index * 70 + "ms");
    });
    chart.classList.add("waiting");
    var observer = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      chart.classList.remove("waiting");
      observer.disconnect();
    }, { rootMargin: "0px 0px -30% 0px" });
    observer.observe(chart);
  }

  // Experiment explorer: filter rows by outcome and text, and show seeds.
  var tools = document.querySelector(".fp-tools");
  if (chart && tools) {
    var kind = "all";
    var corpus = "both";
    var rows = Array.prototype.slice.call(chart.querySelectorAll(".fp-row"));
    var count = tools.querySelector(".fp-count");
    var press = function (buttons, active) {
      buttons.forEach(function (button) {
        button.setAttribute("aria-pressed", String(button === active));
      });
    };
    var matches = function (row) {
      if (kind === "all") return true;
      var cells = corpus === "both" ? [row.dataset.english, row.dataset.code] : [row.dataset[corpus]];
      return cells.indexOf(kind) !== -1;
    };
    var update = function () {
      var shown = 0;
      rows.forEach(function (row) {
        var visible = matches(row);
        row.hidden = !visible;
        if (visible) shown += 1;
      });
      chart.dataset.corpus = corpus;
      count.textContent = "Showing " + shown + " of " + rows.length + " changes";
    };
    var kinds = Array.prototype.slice.call(tools.querySelectorAll("[data-kind]"));
    var corpora = Array.prototype.slice.call(tools.querySelectorAll("[data-corpus]"));
    kinds.forEach(function (button) {
      button.addEventListener("click", function () {
        kind = button.dataset.kind;
        press(kinds, button);
        update();
      });
    });
    corpora.forEach(function (button) {
      button.addEventListener("click", function () {
        corpus = button.dataset.corpus;
        press(corpora, button);
        update();
      });
    });
    var seeds = tools.querySelector("#fp-seeds");
    seeds.addEventListener("click", function () {
      var on = seeds.getAttribute("aria-pressed") !== "true";
      seeds.setAttribute("aria-pressed", String(on));
      chart.classList.toggle("show-seeds", on);
    });
    tools.hidden = false;
    update();
  }

  // GB10 walkthrough: without this script all four stages stay visible.
  var stepper = document.querySelector("[data-stepper]");
  if (stepper) {
    var tablist = stepper.querySelector("[role=tablist]");
    var tabs = Array.prototype.slice.call(stepper.querySelectorAll("[role=tab]"));
    var panels = Array.prototype.slice.call(stepper.querySelectorAll("[role=tabpanel]"));
    var select = function (index, focus) {
      tabs.forEach(function (tab, i) {
        var active = i === index;
        tab.setAttribute("aria-selected", String(active));
        tab.tabIndex = active ? 0 : -1;
        panels[i].hidden = !active;
      });
      if (focus) tabs[index].focus();
    };
    tabs.forEach(function (tab, index) {
      tab.addEventListener("click", function () { select(index, false); });
      tab.addEventListener("keydown", function (event) {
        var step = event.key === "ArrowRight" ? 1 : event.key === "ArrowLeft" ? -1 : 0;
        if (!step) return;
        event.preventDefault();
        select((index + step + tabs.length) % tabs.length, true);
      });
    });
    tablist.hidden = false;
    stepper.classList.add("stepping");
    select(0, false);
  }

  // Call form: compose an email from the visitor's details.
  var form = document.getElementById("call-form");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = new FormData(form);
      var name = data.get("name");
      var company = data.get("company");
      var body = "Hi Yash,\n\n" + data.get("topic") + "\n\nTimes that suit me:\n" + data.get("times") +
        "\n\n" + name + (company ? "\n" + company : "");
      window.location.href = "mailto:bishnoiyash274@gmail.com?subject=" +
        encodeURIComponent("Call with " + name) + "&body=" + encodeURIComponent(body);
    });
  }
})();
