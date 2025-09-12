import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HeroGallery from "./components/HeroGallery";
import HeroDetailPage from "./components/HeroDetailPage";

// Імпортуємо наші дані
import heroesData from "./data/heroes_all.json";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Головна сторінка з галереєю */}
        <Route path="/" element={<HeroGallery heroes={heroesData} />} />

        {/* Сторінка для конкретного героя */}
        <Route
          path="/hero/:id"
          element={<HeroDetailPage heroes={heroesData} />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
