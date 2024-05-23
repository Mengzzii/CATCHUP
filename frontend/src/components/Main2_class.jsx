//여기다가 테스트
import React, { useState, useEffect } from "react";
import styles from "../css/Main2.module.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Cookies } from "react-cookie";
import EditIcon from "../Icons/EditIcon";
import TrashcanIcon from "../Icons/TrashcanIcon";
import Form from "../components/Form";
import Modal from "react-modal";

const Main2_class = () => {
  const cookie = new Cookies();
  const navigate = useNavigate();
  const token = cookie.get("token");
  const [classList, setClassList] = useState({});
  const headers = {
    token: token,
  };
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState("");
  const [cid, setCid] = useState("");
  const [cname, setCname] = useState("");

  const getClassList = async () => {
    await axios
      .get("http://127.0.0.1:8000/user/dashboard", { headers })
      .then((response) => {
        console.log("dashboard 성공:", response.data);
        setClassList(response.data);
      })
      .catch((error) => {
        console.error("dashboard 실패:", error.response.data);
      });
  };

  const deleteclsm = async (classId, headers) => {
    try {
      console.log("classroomid: ", classId);
      console.log("token", token);
      const res = await axios.post(
        `http://127.0.0.1:8000/user/clsm/delete/${classId}`,
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

  const handleDelete = async (classId, headers) => {
    await deleteclsm(classId, headers);
    window.location.replace(`home`);
  };

  const handleClassroom = (id, name) => {
    navigate(`/class/${name}/${id}`);
  };

  const handleEdit = async () => {
    try {
      console.log("msg: ", name);
      const res = await axios.post(
        `http://127.0.0.1:8000/user/clsm/change/${cid}/${name}`,
        null,
        { headers: headers }
      );
      if (res.status != 200) {
        throw new Error("Unable to update classroom name");
      }
      // const data = await res.data;
      // return data;
      // setIsSuccess(true);
    } catch (error) {
      console.error("실패:", error.response.data.detail[0]);
    }
    setIsEditing(false);
    window.location.replace(`/home`);
  };

  useEffect(() => {
    getClassList();
    Modal.setAppElement("#root");
  }, []);

  return (
    <>
      <div className={styles.classes}>
        {Object.entries(classList).map(([id, name]) => (
          <>
            <div className={styles.link} key={id}>
              <div
                className={styles.classchat}
                onClick={() => handleClassroom(id, name)}
              >
                <div className={styles.name}>{name}</div>
                <div className={styles.icons}>
                  <button
                    className={styles.editBt}
                    onClick={(event) => {
                      event.stopPropagation(); // 이벤트 버블링 막음
                      setCid(id);
                      setCname(name);
                      setIsEditing(true);
                    }}
                  >
                    <EditIcon className={styles.edit} />
                  </button>
                  <div>&nbsp;&nbsp;</div>
                  <button
                    className={styles.trashBt}
                    onClick={(event) => {
                      event.stopPropagation();
                      handleDelete(id, headers);
                    }}
                  >
                    <TrashcanIcon className={styles.trashcan} />
                  </button>
                </div>
              </div>
            </div>
          </>
        ))}
        <Modal
          className={styles.modal}
          isOpen={isEditing}
          onRequestClose={() => setIsEditing(false)}
        >
          <div className={styles.ModCon}>
            <div className={styles.ModTop}>
              <h3>강의실 이름 수정하기</h3>
              <div>현재 강의실 : {cname}</div>
            </div>
            <div className={styles.ModInput}>
              <input
                className={styles.textField}
                //value={name}
                onChange={(e) => setName(e.target.value)}
                type={"text"}
                placeholder={"classroom name"}
              ></input>
              {/* <button className={styles.modEditBt} onClick={() => handleEdit()}>
                수정하기
              </button> */}
            </div>
            <div className={styles.ModBtns}>
              <button className={styles.modEditBt} onClick={() => handleEdit()}>
                수정하기
              </button>
              <button
                className={styles.modCloseBt}
                onClick={(event) => {
                  setIsEditing(false);
                  setName("");
                }}
              >
                닫기
              </button>
            </div>
          </div>
        </Modal>
      </div>
    </>
  );
};

export default Main2_class;
