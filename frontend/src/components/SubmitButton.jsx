import styles from "../css/SubmitButton.module.css";

export default function SubmitButton({ message, handleSignUp }) {
  return (
    <div>
      <button className={styles.submitButton} onClick={handleSignUp}>
        {message}
      </button>
    </div>
  );
}
