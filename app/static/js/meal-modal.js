// meal-modal.js

const modalOverlay  = document.getElementById('modalOverlay');
const closeBtn      = document.getElementById('closeBtn');
const modalDayTitle = document.getElementById('modalDayTitle');
const modalMealTitle = document.getElementById('modalMealTitle');

// Common meal fields
const mealName        = document.getElementById('mealName');
const mealTime        = document.getElementById('mealTime');
const mealCalories    = document.getElementById('mealCalories');
const mealIngredients = document.getElementById('mealIngredients');
const mealRecipe      = document.getElementById('mealRecipe');

// Close logic
closeBtn.addEventListener('click', () => {
  modalOverlay.style.display = 'none';
});
modalOverlay.addEventListener('click', (e) => {
  if (e.target === modalOverlay) {
    modalOverlay.style.display = 'none';
  }
});

// For each meal button
document.querySelectorAll('.meal-button').forEach(button => {
  button.addEventListener('click', async () => {
    // Extract day info and meal type
    const year     = button.dataset.year;
    const month    = button.dataset.month;
    const day      = button.dataset.day;
    const mealtype = button.dataset.mealtype; // "lunch" or "dinner"

    // Build the URL (assuming /api/day_details returns {lunch: {}, dinner: {}})
    const url = `/api/day_details?year=${year}&month=${month}&day=${day}`;

    try {
      const response = await fetch(url);
      if (!response.ok) {
        alert(`Error fetching meal data: ${response.statusText}`);
        return;
      }
      const data = await response.json();
      // data = { lunch: {...}, dinner: {...} }

      // Decide which meal object to show
      let mealData = {};
      if (mealtype === "lunch") {
        mealData = data.lunch || {};
        modalMealTitle.textContent = "Lunch";
      } else {
        mealData = data.dinner || {};
        modalMealTitle.textContent = "Dinner";
      }

      // Fill the modal
      modalDayTitle.textContent = `Day ${day}`;
      mealName.textContent     = mealData.name               || '';
      mealTime.textContent     = mealData.prep_time_minutes  || '';
      mealCalories.textContent = mealData.calories_per_person|| '';
      mealRecipe.textContent   = mealData.recipe             || '';

      // Rebuild ingredients list
      mealIngredients.innerHTML = '';
      if (Array.isArray(mealData.ingredients)) {
        mealData.ingredients.forEach(ing => {
          const li = document.createElement('li');
          li.textContent = `${ing.quantity} ${ing.unit} ${ing.name}`;
          mealIngredients.appendChild(li);
        });
      }

      // Show the modal
      modalOverlay.style.display = 'flex';

    } catch (error) {
      console.error(error);
      alert("An unexpected error occurred.");
    }
  });
});
