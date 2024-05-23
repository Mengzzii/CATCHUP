import { React, useRef, useState } from "react";
import styles from "../css/Chat.module.css";
import Trashcan from "../Icons/TrashcanIcon.jsx";
import axios from "axios";
import { Cookies } from "react-cookie";

const deleteclsm = async (classroomid, headers, conceptid) => {
  try {
    console.log("classroomid: ", classroomid);
    console.log("conceptid: ", conceptid);

    const res = await axios.post(
      `http://127.0.0.1:8000/user/clsm/concept/delete/${classroomid}/${conceptid}`,
      null,
      { headers: headers }
    );
    if (res.status != 200) {
      throw new Error("Unable to delete classroom");
    }
    const data = await res.data;
    return data;
  } catch (error) {
    console.error("실패:", error.response.data.detail[0]);
  }
};

const ConceptItem = ({ concept, onClick, classroomid, classroomName }) => {
  const cookie = new Cookies();
  const token = cookie.get("token");
  const headers = {
    token: token,
  };

  const handleDelete = async () => {
    await deleteclsm(classroomid, headers, concept.id);
    window.location.replace(`/class/${classroomName}/${classroomid}`);
  };

  return (
    <div
      className={styles.conceptname}
      onClick={() => onClick(concept.id, concept.name)}
    >
      <div className={styles.conceptL}>&nbsp;{concept.name}</div>
      <div className={styles.conceptR}>
        <button className={styles.trashBt} onClick={handleDelete}>
          <Trashcan className={styles.trashConcept}></Trashcan>
        </button>
      </div>
    </div>
  );
};

export default ConceptItem;
