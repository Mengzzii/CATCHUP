//홈_로그인 전
import { React, useEffect } from "react";
import { Cookies } from "react-cookie";
import Main1_left from "../components/Main1_left";
import Main1_right from "../components/Main1_right";
import styles from "../css/Main1.module.css";

const Main1 = () => {
  const cookie = new Cookies();
  const removeCookie = () => {
    if (cookie.get("token") && cookie.get("name")) {
      cookie.remove("token");
      cookie.remove("name");
      console.log("token과 name 쿠키 삭제");
    }
  };

  useEffect(() => {
    removeCookie();
  });

  return (
    <div className={styles.home}>
      <div className={styles.container}>
        <Main1_left />
        <Main1_right />
      </div>
    </div>
  );
};

export default Main1;
