import React from "react";
import Main1_r_login from "./Main1_r_login";
import Main1_r_signup from "./Main1_r_signup";
import styles from "../css/Main1.module.css";
import { Link } from "react-router-dom";

const Main1_right = () => {
  return (
    <div className={styles.Main1_right}>
      <div className={styles.main2contents}>
        <h1 className={styles.cursor}>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;시작하기
        </h1>
        <br />
        <Link to="/signup">
          <Main1_r_signup />
        </Link>
        &nbsp;&nbsp;&nbsp;
        <Link to="/login">
          <Main1_r_login />
        </Link>
      </div>
    </div>
  );
};

export default Main1_right;
