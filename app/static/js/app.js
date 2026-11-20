(() => {
  // Soft dismiss flashes after a few seconds
  const flashes = document.querySelectorAll(".flash");
  if (flashes.length) {
    setTimeout(() => {
      flashes.forEach((el) => {
        el.style.transition = "opacity 400ms ease, transform 400ms ease";
        el.style.opacity = "0";
        el.style.transform = "translateY(-6px)";
      });
    }, 4200);
  }

  // Prefill today's date on new maintenance form if empty
  const dateInput = document.querySelector('input[name="service_date"]');
  if (dateInput && !dateInput.value) {
    const now = new Date();
    const iso = now.toISOString().slice(0, 10);
    dateInput.value = iso;
  }
})();
