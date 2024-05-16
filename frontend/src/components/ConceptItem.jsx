import React from "react";
import styles from "../css/Chat.module.css";
import Trashcan from "../Icons/TrashcanIcon.jsx";

const ConceptItem = ({ concept, onClick }) => {
  return (
    <div
      className={styles.conceptname}
      onClick={() => onClick(concept.id, concept.name)}
    >
      <div className={styles.conceptL}>&nbsp;{concept.name}</div>
      <div className={styles.conceptR}>
        <button className={styles.trashBt}>
          <Trashcan className={styles.trashConcept}></Trashcan>
        </button>
      </div>
    </div>
  );
};

export default ConceptItem;
