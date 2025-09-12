import React from "react";
import HeroPreviewCard from "./HeroPreviewCard";
import styles from "./HeroGallery.module.css";

const HeroGallery = ({ heroes }) => {
    // console.log(heroes); // Додано для перевірки отриманих даних
  return (
    <div className={styles.galleryContainer}>
      <h1 className={styles.title}>Галерея Героїв</h1>
      <div className={styles.galleryGrid}>
        {heroes.map((hero) => (
          <HeroPreviewCard key={hero.name} hero={hero} />
        ))}
      </div>
    </div>
  );
};

export default HeroGallery;
