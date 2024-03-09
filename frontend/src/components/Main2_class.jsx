//여기다가 테스트
import React, { useState, useEffect } from "react";
import styles from "../css/Main2.module.css";
import { Link } from "react-router-dom";
import getUserId from "../components/Auth.jsx";
import axios from "axios";

const Main2_class = () => {
  // const userId = "mina0104";
  const [userId, setUserId] = useState("");

  useEffect(() => {
    // console.log("useEffect 호출");
    // setUserId(getUserId());
    // console.log("새로운 userId: ", userId);
  }, []);

  const handleCreateNew = async () => {
    const userId = await getUserId();
    console.log("새로운 userId: ", userId);

    const response = await axios.post(
      `http://127.0.0.1:8000/user/classroom/new/${userId}`
    );

    // try {
    //   const response = await axios.post(
    //     `http://127.0.0.1:8000/user/classroom/new/${userId}`
    //   );
    //   if (response) {
    //     console.log("챗방 생성 성공: ", JSON.stringify(response, null, 2));
    //   }
    // } catch (error) {
    //   console.error("챗방 생성 실패: ", error.response.data);
    // }
  };

  return (
    <div>
      <div className={styles.classes}>
        <Link to="/contentchat">
          <div className={styles.classchat} onClick={handleCreateNew}>
            알고리즘
          </div>
        </Link>
        <div className={styles.classchat}>자료 구조</div>
        <div className={styles.classchat}></div>
      </div>
    </div>
  );
};

export default Main2_class;
