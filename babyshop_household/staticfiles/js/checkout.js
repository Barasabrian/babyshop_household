document.addEventListener('DOMContentLoaded', function () {
  // Form validation
  const form = document.getElementById('checkout-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      const paymentMethod = document.querySelector('input[name="payment_method"]:checked').value;

      if (paymentMethod === 'credit_card') {
        const cardNumber = document.getElementById('card_number').value;
        const expiry = document.getElementById('expiry').value;
        const cvc = document.getElementById('cvc').value;

        if (!cardNumber || !expiry || !cvc) {
          e.preventDefault();
          alert('Please complete all credit card fields');
          return false;
        }
      }

      return true;
    });
  }

  // Format credit card input
  const cardNumberInput = document.getElementById('card_number');
  if (cardNumberInput) {
    cardNumberInput.addEventListener('input', function () {
      let value = this.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
      let formatted = '';

      for (let i = 0; i < value.length; i++) {
        if (i > 0 && i % 4 === 0) {
          formatted += ' ';
        }
        formatted += value[i];
      }

      this.value = formatted.substring(0, 19);
    });
  }
});