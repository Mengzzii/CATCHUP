import styles from "../css/SubmitButton.module.css";

export default function SubmitButton({ message }) {
  return (
    <div>
      <button className={styles.submitButton}>{message}</button>
    </div>
  );
}
