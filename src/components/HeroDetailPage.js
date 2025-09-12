import React from "react";
import { useParams } from "react-router-dom";
import styles from "./HeroDetailPage.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faHeart,
  faKhanda,
  faShieldHalved,
  faPersonRunning,
  faStar,
  faBurst,
  faBookSkull,
  faCrosshairs,
} from "@fortawesome/free-solid-svg-icons";

// ... імпорти ...

// const HeroDetailPage = ({ heroes }) => {
//   const { id } = useParams();
//   const hero = heroes.find((h) => h.name === id);
//   console.log(hero.img); // Додано для перевірки отриманих даних

//   if (!hero) {
//     return <div className={styles.notFound}>Героя не знайдено!</div>;
//   }

//   const rarityClassMap = {
//     Легендарний: "legendary",
//     Епічний: "epic",
//     Рідкісний: "rare",
//     Незвичайний: "uncommon",
//     Звичайний: "common",
//   };
//   const rarityClass = styles[rarityClassMap[hero.rarity]] || styles.default;
//   // const imageUrl = `/images/${hero.englishName}.png`;
//   const imageUrl = hero.img;

//   return (
//     <div className={styles.pageContainer}>
//       <div className={`${styles.card} ${rarityClass}`}>
//         {/* Банер рідкісності */}
//         <div
//           className={styles.rarityBanner}
//           style={{ color: styles[rarityClassMap[hero.rarity]] }}
//         >
//           {hero.rarity}
//         </div>

//         <div className={styles.heroImage}>
//           <img src={imageUrl} alt={hero.name} />
//         </div>

//         {/* Іконку фракції можна вставити тут, якщо у вас є локальні зображення */}
//         {/* <div className={styles.heroFaction}>
//                 <img src={`/images/factions/${hero.factionEnglishName}.png`} alt="Faction Icon" />
//             </div> */}

//         <div className={styles.heroName}>
//           <h2>{hero.name}</h2>
//           <p>{hero.title}</p>
//         </div>

//         {/* <div className={styles.statsGrid}>
//           <div className={styles.statItem}>
//             <FontAwesomeIcon icon={faHeart} />
//             <span>ЗДР</span>
//             <strong>{hero.characteristics.hp}</strong>
//           </div>
//           <div className={styles.statItem}>
//             <FontAwesomeIcon icon={faKhanda} />
//             <span>АТК</span>
//             <strong>{hero.characteristics.atk}</strong>
//           </div>
//           <div className={styles.statItem}>
//             <FontAwesomeIcon icon={faShieldHalved} />
//             <span>ЗЩТ</span>
//             <strong>{hero.characteristics.def}</strong>
//           </div>
//           <div className={styles.statItem}>
//             <FontAwesomeIcon icon={faPersonRunning} />
//             <span>ШВД</span>
//             <strong>{hero.characteristics.spd}</strong>
//           </div>
//           <div className={styles.statItem}>
//             <FontAwesomeIcon icon={faStar} />
//             <span>КШ</span>
//             <strong>{hero.characteristics.crate}%</strong>
//           </div>
//           <div className={styles.statItem}>
//             <FontAwesomeIcon icon={faBurst} />
//             <span>КУ</span>
//             <strong>{hero.characteristics.cdmg}%</strong>
//           </div>
//           <div className={styles.statItem}>
//             <FontAwesomeIcon icon={faBookSkull} />
//             <span>ОПР</span>
//             <strong>{hero.characteristics.res}</strong>
//           </div>
//           <div className={styles.statItem}>
//             <FontAwesomeIcon icon={faCrosshairs} />
//             <span>МТК</span>
//             <strong>{hero.characteristics.acc}</strong>
//           </div>
//         </div> */}
//       </div>
//     </div>
//   );
// };

// export default HeroDetailPage;

const HeroDetailPage = ({ heroes }) => {
  const { id } = useParams();
  const hero = heroes.find((h) => h.name === id);
  console.log(hero); // Додано для перевірки отриманих даних

  if (!hero) {
    return <div className={styles.notFound}>Героя не знайдено!</div>;
  }

  const rarityClassMap = {
    Легендарний: "legendary",
    Епічний: "epic",
    Рідкісний: "rare",
    Незвичайний: "uncommon",
    Звичайний: "common",
  };
  const rarityClass = styles[rarityClassMap[hero.rarity]] || styles.default;
  // const imageUrl = `/images/${hero.englishName}.png`;
  const imageUrl = hero.img;

  return (
    <div className={styles.pageContainer}>
      <div className={`${styles.card} ${rarityClass}`}>
        {/* Банер рідкісності */}
        <div
          className={styles.rarityBanner}
          style={{ color: styles[rarityClassMap[hero.rarity]] }}
        >
          {hero.rarity}
        </div>

        <div className={styles.heroImage}>
          <img src={imageUrl} alt={hero.name} />
        </div>

        {/* Іконку фракції можна вставити тут, якщо у вас є локальні зображення */}
        {/* <div className={styles.heroFaction}>
                <img src={`/images/factions/${hero.factionEnglishName}.png`} alt="Faction Icon" />
            </div> */}

        <div className={styles.heroName}>
          <h2>{hero.name}</h2>
          <p>{hero.title}</p>
        </div>

        <div className={styles.statsGrid}>
          <div className={styles.statItem}>
            <FontAwesomeIcon icon={faHeart} />
            <span>LVL</span>
            <strong>{hero.details.en.stats_by_level.LVL}</strong>
          </div>
          <div className={styles.statItem}>
            <FontAwesomeIcon icon={faHeart} />
            <span>STARS</span>
            <strong>{hero.details.en.stats_by_level.STARS}</strong>
          </div>
          <div className={styles.statItem}>
            <FontAwesomeIcon icon={faHeart} />
            <span>HP</span>
            <strong>{hero.details.en.stats_by_level.HP}</strong>
          </div>
          <div className={styles.statItem}>
            <FontAwesomeIcon icon={faHeart} />
            <span>ATK</span>
            <strong>{hero.details.en.stats_by_level.ATK}</strong>
          </div>
          <div className={styles.statItem}>
            <FontAwesomeIcon icon={faHeart} />
            <span>DEF</span>
            <strong>{hero.details.en.stats_by_level.DEF}</strong>
          </div>
          <div className={styles.statItem}>
            <FontAwesomeIcon icon={faHeart} />
            <span>SPD</span>
            <strong>{hero.details.en.stats_by_level.SPD}</strong>
          </div>
          <div className={styles.statItem}>
            <FontAwesomeIcon icon={faHeart} />
            <span>C.RATE</span>
            <strong>{hero.details.en.stats_by_level.C_RATE}</strong>
          </div>

          <div className={styles.statItem}>
            <FontAwesomeIcon icon={faKhanda} />
            <span>C.DMG</span>
            <strong>{hero.details.en.stats_by_level.C_DMG}</strong>
          </div>
          <div className={styles.statItem}>
            <FontAwesomeIcon icon={faShieldHalved} />
            <span>RESIST</span>
            <strong>{hero.details.en.stats_by_level.RESIST}</strong>
          </div>
          <div className={styles.statItem}>
            <FontAwesomeIcon icon={faShieldHalved} />
            <span>ACC</span>
            <strong>{hero.details.en.stats_by_level.ACC}</strong>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroDetailPage;
