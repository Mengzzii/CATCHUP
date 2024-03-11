//여기다가 테스트
import React, { useState, useEffect } from "react";
import styles from "../css/Main2.module.css";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { Cookies } from "react-cookie";

const Main2_class = () => {
  const cookie = new Cookies();
  const navigate = useNavigate();
  const [classList, setClassList] = useState({});

  const getClassList = async () => {
    const token = cookie.get("token");
    const headers = {
      token: token,
    };
    await axios
      .get("http://127.0.0.1:8000/user/dashboard", { headers })
      .then((response) => {
        console.log("생성 성공:", response.data);
        // for (var key in response.data) {
        //   console.log(key);
        //   console.log(response.data[key]);
        // }
        setClassList(response.data);
      })
      .catch((error) => {
        console.error("생성 실패:", error.response.data);
      });
  };

  useEffect(() => {
    getClassList();
  }, []);

  return (
    <div className={styles.classes}>
      {Object.entries(classList).map(([id, name]) => (
        <Link to={`/chat/${id}`} key={id}>
          <div className={styles.classchat}>{name}</div>
        </Link>
      ))}
    </div>
  );
};

export default Main2_class;
