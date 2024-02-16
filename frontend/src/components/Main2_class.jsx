import React from "react";
import styles from "../css/Main2.module.css";
import { Link } from "react-router-dom";

const Main2_class = () => {
  return (
    <div>
      <div className={styles.classes}>
        <Link to="/contentchat">
          <div className={styles.classchat}>알고리즘</div>
        </Link>
        <div className={styles.classchat}>자료 구조</div>
        <div className={styles.classchat}></div>
      </div>
    </div>
  );
};

export default Main2_class;
