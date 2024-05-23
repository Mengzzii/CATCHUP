import React from "react";
import styles from "../css/Loading.module.css";
import Spinner from "./Spinner.gif";

export default ({ text }) => {
  return (
    <div className={styles.background} style={{ whiteSpace: "pre-line" }}>
      <img src={Spinner} alt="로딩중" width="5%" />
      <div className={styles.loadingText}>{text}</div>
    </div>
  );
};
