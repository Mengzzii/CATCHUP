import styles from "../css/Form.module.css";
import { useState } from "react";

export default function Form({ text, message }) {
  const [input, setInput] = useState("");
  return (
    <div>
      <span className={styles.message}>{message}</span>
      <br />
      <input
        className={styles.textField}
        onChange={(e) => setInput(input)}
        type="text"
        placeholder={text}
      ></input>
    </div>
  );
}
