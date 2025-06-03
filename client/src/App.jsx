import React, { useState, useEffect } from 'react';
import './App.css';

function RecipeShimmer() {
  return (
    <div className="recipe-card shimmer">
      <div className="shimmer-title shimmer-anim"></div>
      <div className="shimmer-meta shimmer-anim"></div>
      <div className="shimmer-section shimmer-anim"></div>
      <div className="shimmer-section shimmer-anim"></div>
      <div className="shimmer-section shimmer-anim"></div>
    </div>
  );
}

function App() {
  const [ingredients, setIngredients] = useState('');
  const [recipe, setRecipe] = useState(null);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [favorites, setFavorites] = useState([]);
  const [loadingFav, setLoadingFav] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    document.body.className = darkMode ? 'dark' : '';
  }, [darkMode]);

  // Fetch favorites on mount
  useEffect(() => {
    fetchFavorites();
  }, []);

  const fetchFavorites = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/favorites');
      const data = await res.json();
      setFavorites(data || []);
    } catch (err) {
      setFavorites([]);
    }
  };

  const generateRecipe = async () => {
    setSaved(false);
    setRecipe(null);
    setIngredients("");
    setError('');
    setLoading(true); // Start loading

    try {
      const response = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ingredients })
      });
      const data = await response.json();
      if (data.error) setError(data.error);
      else setRecipe(data);
    } catch (err) {
      setError('Failed to fetch recipe.');
    }
    setLoading(false); // End loading
  };

  const saveToFavorites = async () => {
      // Check for duplicate by title (case-insensitive)
  if (
    recipe &&
    favorites.some(
      (fav) => fav.title.trim().toLowerCase() === recipe.title.trim().toLowerCase()
    )
  ) {
    alert('Recipe is already present inside favorites');
    return;
  }



    try {
      const response = await fetch('http://localhost:5000/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(recipe)
      });
      const result = await response.json();
      if (result.message) {
        setSaved(true);
        fetchFavorites(); // Refresh favorites list
      }
    } catch (err) {
      console.error('Failed to save recipe');
    }
  };

  
  return (
    <div className="app">
      <button className="toggle" onClick={() => setDarkMode(!darkMode)}>
        {darkMode ? '🌞 Light Mode' : '🌙 Dark Mode'}
      </button>

      <h1 className="title">🍽️ AI Recipe Chef👨‍🍳Master</h1>

      <textarea
        placeholder="Enter ingredients (e.g., tomato, garlic, oats)"
        value={ingredients}
        onChange={(e) => setIngredients(e.target.value)}
      />
      <button onClick={generateRecipe}>Generate Recipe</button>

      {error && <p className="error">{error}</p>}
      {loading && <RecipeShimmer />}

      {!loading && recipe && (
        <div className="recipe-card">
          <span
            className={`heart ${saved ? 'saved' : ''}`}
            title="Save to favorites"
            onClick={saveToFavorites}
          >
            ❤️
          </span>

          <h2 className="recipe-title">{recipe.title}</h2>
          <div className="meta">
            <span>⏱ {recipe.prep_time}</span>
            <span>👨‍🍳 {recipe.servings}</span>
          </div>

          <section>
            <h3>📝 Ingredients</h3>
            <ul>{recipe.ingredients.map((item, i) => <li key={i}>{item}</li>)}</ul>
          </section>

          <section>
            <h3>👨‍🍳 Steps</h3>
            <ol>{recipe.steps.map((step, i) => <li key={i}>{step}</li>)}</ol>
          </section>

          <section>
            <h3>✨ Tips & Variations</h3>
            <ul>{recipe.tips.map((tip, i) => <li key={i}>{tip}</li>)}</ul>
          </section>
        </div>
      )}

      {/* Favorites Section */}
      <div className="favorites-section">
        <h3 className="favorites-title">⭐ Favorite Recipes</h3>
        {favorites.length === 0 ? (
          <div className="favorites-empty">No favorites yet.</div>
        ) : (
          <div className="favorites-list">
            {favorites.map((fav) => (
              <button
                key={fav.title}
                className="favorite-chip"
                onClick={() => setRecipe(fav)}
                disabled={loadingFav}
              >
                {fav.title}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;