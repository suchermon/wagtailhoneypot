let submitBtn = document.querySelector('[type="submit"]');

if(submitBtn.length) {
  submitBtn.addEventListener('click', function(e) {
    document.querySelectorAll('[data-js="hp-formfield"]').forEach(el => el.removeAttribute('required'));
  });
}
