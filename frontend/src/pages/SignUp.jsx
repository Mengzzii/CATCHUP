import Form from "../components/Form";
import Logo from "../components/Logo";
import SubmitButton from "../components/SubmitButton";
import styles from "../css/SignUp.module.css";
import React, { useState } from "react";
import axios from "axios";

export default function SignUp() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [id, setId] = useState("");
  const [password, setPassword] = useState("");

  const handleSignUp = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/user/signup", {
        name: name,
        email: email,
        id: id,
        password: password,
      });
      console.log("회원가입 성공:", response.data);
    } catch (error) {
      console.error("회원가입 실패:", error.response.data);
    }
  };

  return (
    <div className={styles.body}>
      <span className={styles.logo}>
        <Logo />
      </span>
      <br />
      <div>
        <Form message={"이름"} setInput={setName} />
      </div>
      <br />
      <div>
        <Form message={"이메일"} setInput={setEmail} />
      </div>
      <br />
      <div>
        <Form message={"아이디"} setInput={setId} />
      </div>
      <br />
      <div>
        <Form message={"비밀번호"} setInput={setPassword} />
      </div>
      <br />
      <br />
      <span className={styles.loginButton}>
        <SubmitButton message={"회원가입"} handleSignUp={handleSignUp} />
      </span>
    </div>
  );
}
