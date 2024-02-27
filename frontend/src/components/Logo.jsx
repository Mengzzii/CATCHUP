import styles from "../css/Logo.module.css";
import { Link, useNavigate } from "react-router-dom";
import { Cookies } from "react-cookie";

export default function Logo() {
  const cookie = new Cookies();
  const navigate = useNavigate();

  const goHome = () => {
    navigate("/");
  };

  return (
    <div>
      <h1 className={styles.logo} onClick={goHome}>
        CATCHUP
      </h1>
    </div>
  );
}
