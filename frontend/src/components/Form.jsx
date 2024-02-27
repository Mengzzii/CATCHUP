import styles from "../css/Form.module.css";
import { useState } from "react";

export default function Form({ text, message, setInput, inputType }) {
  return (
    <div>
      <span className={styles.message}>{message}</span>
      <br />
      <input
        className={styles.textField}
        onChange={(e) => setInput(e.target.value)}
        type={"text" && inputType}
        placeholder={text}
      ></input>
    </div>
  );
}
