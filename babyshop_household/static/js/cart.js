document.addEventListener('DOMContentLoaded', function () {
  // Update quantity in cart
  document.querySelectorAll('.update-quantity').forEach(input => {
    input.addEventListener('change', function () {
      const form = this.closest('form');
      if (form) {
        form.submit();
      }
    });
  });

  // Remove item from cart
  document.querySelectorAll('.remove-item').forEach(button => {
    button.addEventListener('click', function (e) {
      e.preventDefault();
      if (confirm('Are you sure you want to remove this item from your cart?')) {
        const form = this.closest('form');
        if (form) {
          form.submit();
        }
      }
    });
  });
});