import React from "react";
import styles from "./HeroPreviewCard.module.css";

const HeroPreviewCard = ({ hero }) => {
  // Ваш JSON використовує українські назви рідкісності,
  // тому нам потрібно перетворити їх на класи CSS.
  const rarityClassMap = {
    Легендарний: "legendary",
    Епічний: "epic",
    Рідкісний: "rare",
    Незвичайний: "uncommon",
    Звичайний: "common", // Додамо клас для звичайних
  };
//   console.log(hero.img); // Додано для перевірки отриманих даних

  // Використовуємо англійську назву для посилання, бо вона унікальна і без пробілів
    const heroId = hero.name;
    // console.log(heroId); // Додано для перевірки heroId
  const rarityClass = styles[rarityClassMap[hero.class]] || styles.default;

  // Шлях до зображення тепер інший
        // Новий код (виправлено)
    const imageUrl = hero.img;
    // console.log(imageUrl); // Додано для перевірки шляху до зображення

  return (
    <a
      href={`/hero/${heroId}`}
      target="_blank"
      rel="noopener noreferrer"
      className={`${styles.card} ${rarityClass}`}
    >
      <img src={hero.img} alt={hero.name} className={styles.heroImage} />
      <div className={styles.heroName}>{hero.name}</div>
    </a>
  );
};

export default HeroPreviewCard;
