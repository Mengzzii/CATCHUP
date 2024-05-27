import React, { useState, useEffect } from "react";
import styles from "../css/Main2.module.css";
import { Link, useNavigate } from "react-router-dom";
import { Cookies } from "react-cookie";
import axios from "axios";

const Main2_new = () => {
  const navigate = useNavigate();
  const cookie = new Cookies();

  const handleNewClassroom = async () => {
    const token = cookie.get("token");
    const headers = {
      token: token,
    };

    await axios
      .post(`${import.meta.env.VITE_BACKEND_URL}/user/classroom/new`, null, { headers })
      .then((response) => {
        console.log("생성 성공:", response.data);
        const classid = response.data;
        navigate(`/new/class/${classid}`);
      })
      .catch((error) => {
        console.error("생성 실패:", error.response.data);
      });
  };

  return (
    <button className={styles.newbtn} onClick={handleNewClassroom}>
      +
    </button>
  );
};

export default Main2_new;
