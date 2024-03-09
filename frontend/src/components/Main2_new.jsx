import React, { useState, useEffect } from "react";
import styles from "../css/Main2.module.css";
import { Link } from "react-router-dom";

const Main2_new = () => {
  return (
    <Link to="/classchat">
      <button className={styles.newbtn}>+</button>
    </Link>
  );
};

export default Main2_new;
