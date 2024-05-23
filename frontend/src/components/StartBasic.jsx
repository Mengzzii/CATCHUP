import React from "react";
import styles from "../css/ChatExtra.module.css";

const StartBasic = ({ UserName }) => {
  return (
    <div className={styles.container}>
      <div>
        <span className={styles.userText}>{UserName}</span>&nbsp;님 환영합니다!
      </div>
      <div>공부하고 싶으신 과목을 입력해주세요!</div>
      {/* <div>
        <span className={styles.userText}>{currentRoom}</span>&nbsp;공부를
        시작하시겠어요?
      </div> */}
      {/* <button className={styles.startBt} onClick={onClick}>
        공부 시작하기
      </button> */}
    </div>
  );
};

export default StartBasic;

//onClick, UserName, classroom, currentRoom
