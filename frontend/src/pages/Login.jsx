import { Link, useNavigate } from "react-router-dom";
import React, { useState, useEffect } from "react";
import axios from "axios";
import Form from "../components/Form";
import Logo from "../components/Logo";
import NormalButton from "../components/NormalButton";
import Bstyles from "../css/NormalButton.module.css";
import styles from "../css/Login.module.css";
import { Cookies } from "react-cookie";

export default function Login() {
  const [id, setId] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isError, setIsError] = useState(0);
  const navigate = useNavigate();
  const cookie = new Cookies();

  const removeCookie = () => {
    if (cookie.get("token") && cookie.get("name")) {
      cookie.remove("token");
      cookie.remove("name");
      console.log("token과 name 쿠키 삭제");
    }
  };

  const handleOnSubmit = async (e) => {
    e.preventDefault();
    setIsError(0);
    try {
      const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/user/login`, {
        name: "",
        email: "dummy@email.com",
        id: id,
        password: password,
      });
      console.log("로그인 성공:", response.data);
      cookie.set("token", response.data.token);
      cookie.set("name", response.data.name);
      navigate("/home");
    } catch (error) {
      console.error("로그인 실패:", error.response.data);
      setIsError(1);
      setErrorMessage(
        `아이디 또는 비밀번호를 잘못 입력했습니다. 입력하신 내용을 다시 확인해주세요.`
      );
    }
  };

  useEffect(() => {
    removeCookie();
  });

  return (
    <div className={styles.body}>
      <span className={styles.logo}>
        <Logo />
      </span>
      <br />
      <form onSubmit={handleOnSubmit}>
        <div className={styles.input}>
          <div>
            <Form text="아이디" setInput={setId} />
          </div>
          <br />
          <div>
            <Form text="비밀번호" setInput={setPassword} inputType="password" />
          </div>
        </div>
        <br />
        <br />
        <button className={Bstyles.NormalButton}>로그인</button>
        {/* <NormalButton message={"로그인"} onClick={handleLogin} /> */}
        <Link to="/signup" className={styles.signup}>
          <h5>회원가입</h5>
        </Link>
        {/* {errorMessage && <div>{errorMessage}</div>} */}
        {isError ? <div className={styles.fadeout}>{errorMessage}</div> : null}
      </form>
    </div>
  );
}
