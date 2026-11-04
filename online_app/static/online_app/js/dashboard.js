/**
 * Online LMS - Dashboard JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
  // Metric counter animation
  const counters = document.querySelectorAll('.counter-anim');
  counters.forEach(counter => {
    const target = +counter.getAttribute('data-target') || +counter.innerText;
    let count = 0;
    const speed = 25;
    const updateCount = () => {
      const inc = Math.max(1, Math.ceil(target / speed));
      count += inc;
      if (count < target) {
        counter.innerText = count;
        setTimeout(updateCount, 20);
      } else {
        counter.innerText = target;
      }
    };
    if (target > 0) {
      counter.innerText = '0';
      updateCount();
    }
  });
});

