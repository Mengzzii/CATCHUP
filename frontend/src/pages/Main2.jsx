//"/home"_로그인 후 홈화면
import { React } from "react";
import useCheckLogin from "../hooks/useCheckLogin";
import Main2_top from "../components/Main2_top";
import Main2_new from "../components/Main2_new";
import Main2_class from "../components/Main2_class";
import styles from "../css/Main2.module.css";
import stylesL from "../css/Logo.module.css";

function Main2() {
  useCheckLogin();

  return (
    <div className={styles.home}>
      <div className={styles.container}>
        <div className={styles.top}>
          <Main2_top />
        </div>
        <div className={styles.logo}>
          <div className={stylesL.logo_main2}>CATCHUP</div>
        </div>
        <div className={styles.middle}>
          <Main2_class />
        </div>
        <div className={styles.bottom}>
          <Main2_new />
        </div>
      </div>
    </div>
  );
}

export default Main2;
