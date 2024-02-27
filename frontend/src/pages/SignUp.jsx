import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Modal from "react-modal";
import axios from "axios";
import Form from "../components/Form";
import Logo from "../components/Logo";
import SubmitButton from "../components/SubmitButton";
import NormalButton from "../components/NormalButton";
import styles from "../css/SignUp.module.css";

export default function SignUp() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [id, setId] = useState("");
  const [password, setPassword] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    Modal.setAppElement("#root");
  }, []);

  const handleSignUp = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/user/signup", {
        name: name,
        email: email,
        id: id,
        password: password,
      });
      console.log("회원가입 성공:", response.data);
      setIsSuccess(true);
      setErrorMessage("");
    } catch (error) {
      console.error("회원가입 실패:", error.response.data);
      setErrorMessage("회원가입이 실패하였습니다.");
    }
  };

  const handleLogin = () => {
    navigate("/login");
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
        <Form
          message={"비밀번호"}
          setInput={setPassword}
          inputType="password"
        />
      </div>
      <br />
      <br />
      <span>
        <SubmitButton message={"회원가입"} handleSignUp={handleSignUp} />
      </span>

      <Modal
        className={styles.modal}
        isOpen={isSuccess}
        onRequestClose={() => setIsSuccess(false)}
      >
        <h2>회원가입 완료되었습니다!</h2>
        <div className={styles.loginButton}>
          <NormalButton message={"로그인 하기"} onClick={handleLogin} />
        </div>
      </Modal>

      <br />
      {errorMessage && (
        <div className={styles.errorMessage}>{errorMessage}</div>
      )}
    </div>
  );
}
