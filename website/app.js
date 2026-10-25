/* SmartCart demo interactions + GTM dataLayer events.
   No real customer details or payment information are collected. */
window.dataLayer = window.dataLayer || [];

const cart = new Map();
const productCards = [...document.querySelectorAll(".product-card")];
const cartPanel = document.querySelector("#cart-panel");
const cartItems = document.querySelector("#cart-items");
const cartTotal = document.querySelector("#cart-total");
const cartCount = document.querySelector("#cart-count");
const confirmation = document.querySelector("#confirmation");
const toast = document.querySelector("#toast");

function pushEvent(eventName, params = {}) {
  const payload = { event: eventName, ...params };
  window.dataLayer.push(payload);
  console.info("[SmartCart dataLayer]", payload);
}

function productFromCard(card) {
  return {
    item_id: card.dataset.id,
    item_name: card.dataset.name,
    price: Number(card.dataset.price),
    quantity: 1
  };
}

function itemsInCart() {
  return [...cart.values()].map(item => ({...item}));
}

function totalValue() {
  return itemsInCart().reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 1800);
}

function renderCart() {
  const items = itemsInCart();
  cartCount.textContent = items.reduce((sum, item) => sum + item.quantity, 0);
  if (!items.length) {
    cartItems.innerHTML = "<p>Your cart is empty.</p>";
  } else {
    cartItems.innerHTML = items.map(item =>
      `<div class="cart-row"><span>${item.item_name} × ${item.quantity}</span><strong>₹${(item.price * item.quantity).toLocaleString("en-IN")}</strong></div>`
    ).join("");
  }
  cartTotal.textContent = `Total: ₹${totalValue().toLocaleString("en-IN")}`;
}

productCards.forEach(card => {
  const product = productFromCard(card);
  // Track product detail visibility when the product card enters the page.
  // For this small demo, each card is counted as viewed on initial page load.
  pushEvent("view_item", {
    currency: "INR",
    value: product.price,
    ecommerce: { currency: "INR", value: product.price, items: [product] }
  });

  card.querySelector(".add-button").addEventListener("click", () => {
    const existing = cart.get(product.item_id);
    if (existing) existing.quantity += 1;
    else cart.set(product.item_id, {...product});
    const added = cart.get(product.item_id);
    pushEvent("add_to_cart", {
      currency: "INR",
      value: added.price,
      ecommerce: {
        currency: "INR",
        value: added.price,
        items: [{...added, quantity: 1}]
      }
    });
    renderCart();
    showToast(`${product.item_name} added to cart`);
  });
});

function openCart() {
  cartPanel.hidden = false;
  confirmation.hidden = true;
  cartPanel.scrollIntoView({behavior: "smooth", block: "start"});
  pushEvent("view_cart", {
    currency: "INR",
    value: totalValue(),
    ecommerce: { currency: "INR", value: totalValue(), items: itemsInCart() }
  });
}

document.querySelector("#view-cart-button").addEventListener("click", openCart);
document.querySelector("#close-cart").addEventListener("click", () => {
  cartPanel.hidden = true;
  document.querySelector("#products").scrollIntoView({behavior: "smooth"});
});

document.querySelector("#checkout-button").addEventListener("click", () => {
  if (!cart.size) {
    showToast("Add a product before checkout");
    return;
  }
  pushEvent("begin_checkout", {
    currency: "INR",
    value: totalValue(),
    ecommerce: { currency: "INR", value: totalValue(), items: itemsInCart() }
  });
  // This is a simulated checkout; no payment details are requested.
  const orderId = `DEMO-${Date.now()}`;
  pushEvent("purchase", {
    transaction_id: orderId,
    currency: "INR",
    value: totalValue(),
    tax: 0,
    shipping: 0,
    ecommerce: {
      transaction_id: orderId,
      currency: "INR",
      value: totalValue(),
      tax: 0,
      shipping: 0,
      items: itemsInCart()
    }
  });
  cart.clear();
  renderCart();
  cartPanel.hidden = true;
  confirmation.hidden = false;
  confirmation.scrollIntoView({behavior: "smooth", block: "start"});
});

document.querySelector("#continue-button").addEventListener("click", () => {
  confirmation.hidden = true;
  document.querySelector("#products").scrollIntoView({behavior: "smooth"});
});

document.querySelector("#shop-now").addEventListener("click", () => {
  pushEvent("select_promotion", {
    promotion_name: "homepage_hero",
    creative_name: "Explore products"
  });
});

renderCart();
