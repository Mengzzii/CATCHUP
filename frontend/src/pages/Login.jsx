import { Link, useNavigate } from "react-router-dom";
import { React, useState, useEffect } from "react";
import axios from "axios";
import Form from "../components/Form";
import Logo from "../components/Logo";
import NormalButton from "../components/NormalButton";
import styles from "../css/Login.module.css";
import { Cookies } from "react-cookie";

export default function Login() {
  const [id, setId] = useState("");
  const [password, setPassword] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  const cookie = new Cookies();

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/user/login", {
        name: "",
        email: "dummy@email.com",
        id: id,
        password: password,
      });
      console.log("로그인 성공:", response.data);
      cookie.set("token", response.data.token);
      setIsSuccess(true);
      navigate("/home");
    } catch (error) {
      console.error("로그인 실패:", error.response.data);
      setErrorMessage(
        "아이디(로그인 전용 아이디) 또는 비밀번호를 잘못 입력했습니다. 입력하신 내용을 다시 확인해주세요."
      );
    }
  };

  return (
    <div className={styles.body}>
      <span className={styles.logo}>
        <Logo />
      </span>
      <br />
      <div className={styles.input}>
        <div>
          <Form text="아이디" setInput={setId} />
        </div>
        <br />
        <div>
          <Form text="비밀번호" setInput={setPassword} />
        </div>
      </div>
      <br />
      <br />
      <NormalButton message={"로그인"} onClick={handleLogin} />
      <Link to="/signup" className={styles.signup}>
        <h5>회원가입</h5>
      </Link>
      {errorMessage && <div>{errorMessage}</div>}
    </div>
  );
}
