import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Cookies } from "react-cookie";
import styles from "../css/Main2.module.css";
import axios from "axios";

const Main2_top = () => {
  const cookie = new Cookies();
  const navigate = useNavigate();

  const logOut = () => {
    cookie.remove("token");
    cookie.remove("name");
    navigate("/");
  };

  const newTest = async () => {
    const token = cookie.get("token");
    const headers = {
      token: token,
    };

    await axios
      .post("http://127.0.0.1:8000/user/test/classroom/new", null, { headers })
      .then((response) => {
        console.log("생성 성공:", response.data);
      })
      .catch((error) => {
        console.error("생성 실패:", error.response.data);
      });
  };

  return (
    <>
      <button className={styles.logoutBt} onClick={logOut}>
        로그아웃
      </button>
      &nbsp;&nbsp;
      <div className={styles.cursor} onClick={newTest}>
        {cookie.get("name")} 님
      </div>
      &nbsp;&nbsp;
      <svg
        className={styles.userIc}
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
      >
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" />
      </svg>
    </>
  );
};

export default Main2_top;
