import styles from "../css/NormalButton.module.css";

export default function NormalButton({ message, onClick }) {
  return (
    <div>
      <button className={styles.NormalButton} onClick={onClick}>
        {message}
      </button>
    </div>
  );
}
