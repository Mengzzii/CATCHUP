import React from "react";
import styles from "../css/Main1.module.css";
import stylesL from "../css/Logo.module.css";

const Main1_left = () => {
  return (
    <div className={styles.Main1_left}>
      <header className={stylesL.logo_small}>CATCHUP</header>
      <div className={styles.text}>
        부족한 전공 기초 지식 <br />
        하루에 한 개념씩 따라잡기 .
      </div>
    </div>
  );
};

export default Main1_left;
