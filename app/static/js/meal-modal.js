// meal-modal.js

// Grab references to modal elements
const modalOverlay   = document.getElementById('modalOverlay');
const closeBtn       = document.getElementById('closeBtn');
const modalDayTitle  = document.getElementById('modalDayTitle');

// Lunch fields
const lunchName        = document.getElementById('lunchName');
const lunchTime        = document.getElementById('lunchTime');
const lunchCalories    = document.getElementById('lunchCalories');
const lunchIngredients = document.getElementById('lunchIngredients');
const lunchRecipe      = document.getElementById('lunchRecipe');

// Dinner fields
const dinnerName        = document.getElementById('dinnerName');
const dinnerTime        = document.getElementById('dinnerTime');
const dinnerCalories    = document.getElementById('dinnerCalories');
const dinnerIngredients = document.getElementById('dinnerIngredients');
const dinnerRecipe      = document.getElementById('dinnerRecipe');

// Close button logic
closeBtn.addEventListener('click', () => {
  modalOverlay.style.display = 'none';
});

// If user clicks outside the white modal box (on the dark overlay), close
modalOverlay.addEventListener('click', (e) => {
  if (e.target === modalOverlay) {
    modalOverlay.style.display = 'none';
  }
});

// Attach click events to each day box
document.querySelectorAll('.day-box').forEach(box => {
  box.addEventListener('click', async () => {
    // 1) Extract year/month/day from the box's data attributes
    const year  = box.dataset.year;
    const month = box.dataset.month;
    const day   = box.dataset.day;

    // 2) Build the API endpoint URL (adjust if your endpoint is different)
    const url = `/api/day_details?year=${year}&month=${month}&day=${day}`;

    // 3) Fetch the full meal data from the server
    try {
      const response = await fetch(url);
      if (!response.ok) {
        alert(`Error fetching data: ${response.statusText}`);
        return;
      }
      const data = await response.json();

      // data should look like:
      // {
      //   lunch: {...},
      //   dinner: {...}
      // }

      // 4) Populate the modal fields

      // Title
      modalDayTitle.textContent = `Day ${day}`;

      // Lunch
      const lunch = data.lunch || {};
      lunchName.textContent     = lunch.name               || '';
      lunchTime.textContent     = lunch.prep_time_minutes  || '';
      lunchCalories.textContent = lunch.calories_per_person|| '';
      lunchRecipe.textContent   = lunch.recipe             || '';

      // Clear old ingredients
      lunchIngredients.innerHTML = '';
      if (Array.isArray(lunch.ingredients)) {
        lunch.ingredients.forEach(ing => {
          const li = document.createElement('li');
          li.textContent = `${ing.quantity} ${ing.unit} ${ing.name}`;
          lunchIngredients.appendChild(li);
        });
      }

      // Dinner
      const dinner = data.dinner || {};
      dinnerName.textContent     = dinner.name               || '';
      dinnerTime.textContent     = dinner.prep_time_minutes  || '';
      dinnerCalories.textContent = dinner.calories_per_person|| '';
      dinnerRecipe.textContent   = dinner.recipe             || '';

      // Clear old ingredients
      dinnerIngredients.innerHTML = '';
      if (Array.isArray(dinner.ingredients)) {
        dinner.ingredients.forEach(ing => {
          const li = document.createElement('li');
          li.textContent = `${ing.quantity} ${ing.unit} ${ing.name}`;
          dinnerIngredients.appendChild(li);
        });
      }

      // 5) Show the modal
      modalOverlay.style.display = 'flex';
    } catch (error) {
      console.error(error);
      alert("An unexpected error occurred.");
    }
  });
});
