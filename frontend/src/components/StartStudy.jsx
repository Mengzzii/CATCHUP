import React from "react";
import styles from "../css/ChatExtra.module.css";

const StartStudy = ({ onClick, UserName, classroom, currentRoom }) => {
  return (
    <div className={styles.container}>
      <div>
        <span className={styles.userText}>{UserName}</span>&nbsp;님 환영합니다!
      </div>
      <div>
        <span className={styles.userText}>{classroom}</span>&nbsp;과목을
        따라잡고 싶으시군요!
      </div>
      <div>
        <span className={styles.userText}>{currentRoom}</span>&nbsp;공부를
        시작하시겠어요?
      </div>
      <button className={styles.startBt} onClick={onClick}>
        공부 시작하기
      </button>
    </div>
  );
};

export default StartStudy;
