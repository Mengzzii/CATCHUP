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
  const handleClassroom = async (id) => {
    navigate(`/class/${id}`);
  };

  const getClassList = async () => {
    const token = cookie.get("token");
    const headers = {
      token: token,
    };

    await axios
      .get("http://127.0.0.1:8000/user/dashboard", { headers })
      .then((response) => {
        console.log("dashboard 성공:", response.data);
        setClassList(response.data);
      })
      .catch((error) => {
        console.error("dashboard 실패:", error.response.data);
      });
  };

  useEffect(() => {
    getClassList();
  }, []);

  return (
    <div className={styles.classes}>
      {Object.entries(classList).map(([id, name]) => (
        <Link to={`/class/${id}`} key={id}>
          <div className={styles.classchat}>{name}</div>
        </Link>
        // <button className={styles.classchat} onClick={handleClassroom(id)}>
        //   {name}
        // </button>
      ))}
    </div>
  );
};

export default Main2_class;
