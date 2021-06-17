let submitBtn = document.querySelector('[type="submit"]');

if(submitBtn !== null) {
  submitBtn.addEventListener('click', function(e) {
    document.querySelectorAll('[data-js="hp-formfield"]').forEach(el => el.removeAttribute('required'));
  });
}
