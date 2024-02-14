import { Link } from "react-router-dom";
import Form from "../components/Form";
import Logo from "../components/Logo";
import SubmitButton from "../components/SubmitButton";
import styles from "../css/Login.module.css";

export default function Login() {
  return (
    <div className={styles.body}>
      <span className={styles.logo}>
        <Logo />
      </span>
      <br />
      <div className={styles.input}>
        <div>
          <Form text="아이디" />
        </div>
        <br />
        <div>
          <Form text="비밀번호" />
        </div>
      </div>
      <br />
      <br />
      <SubmitButton message={"로그인"} />
      <Link to="/signup" className={styles.signup}>
        <h5>회원가입</h5>
      </Link>
    </div>
  );
}
