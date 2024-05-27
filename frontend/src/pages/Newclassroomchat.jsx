// "/new/class/${classid}"
import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import useCheckLogin from "../hooks/useCheckLogin";
import ChatItem from "../components/ChatItem";
import ConceptItem from "../components/ConceptItem";
import axios from "axios";
import { IoMdSend } from "react-icons/io";
import { Cookies } from "react-cookie";
import { useParams } from "react-router-dom";
import styles from "../css/Chat.module.css";
import StylesL from "../css/Logo.module.css";
import { useNavigate } from "react-router-dom";
import HomeLogo2 from "../components/HomeLogo2.jsx";

const getUserChats = async (classid, headers) => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/user/getallchats`, {
      params: { classroom_id: classid },
      headers: headers,
    });
    console.log(res.data);
    if (res.status !== 200) {
      throw new Error("Unable to send chat");
    }

    return res.data;
  } catch (error) {
    console.error("실패:", error.response.data.detail[0]);
  }
};

const getClassConcepts = async (classid, headers) => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/chat/getclassconcepts`, {
      params: { classroom_id: classid },
      headers: headers,
    });
    if (res.status !== 200) {
      throw new Error("Unable to send chat");
    }
    console.log("Response:", JSON.stringify(res, null, 2));
    const data = await res.data;
    return data;
  } catch (error) {
    console.error("실패:", error.response.data.detail[0]);
  }
};

// concept별 chat 가져온다.
const getConceptChats = async (classid, headers, concept_id) => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/getconceptchats`, {
      params: { classroom_id: classid, concept_id: concept_id },
      headers: headers,
    });
    if (res.status !== 200) {
      throw new Error("Unable to send chat");
    }
    console.log("get Concept Chats / Response:", JSON.stringify(res, null, 2));
    const data = await res.data;
    return data;
  } catch (error) {
    console.error("실패:", error.response.data.detail[0]);
  }
};

// chat의 종류를 isConceptChat 값을 통해 구분한다.
// conceptchat일 경우: 질문챗으로 간주, 헤당하는 백의 엔드포인트 호출
// conceptchat이 아닐 경우: 기본챗방: 목록받아오는 백의 엔드포인드 호출
const sendChatRequest = async (isConceptChat, classid, msg, headers) => {
  console.log(isConceptChat);
  if (isConceptChat) {
    const concept_id = isConceptChat;
    try {
      const res = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/chat/concept/qna/${classid}/${msg}/${concept_id}`,
        null,
        { headers: headers }
      );
      const data = await res.data;
      console.log("Response:", JSON.stringify(data, null, 2));
      return data;
    } catch (error) {
      console.error("실패:", error.response.data);
    }
  } else {
    try {
      const res = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/chat/new/${classid}/${msg}`,
        null,
        { headers: headers }
      );
      const data = await res.data;
      console.log("Response:", JSON.stringify(data, null, 2));
      window.location.replace(`/new/class/${classid}`);
      // setRefresh((refresh) => refresh * -1);
      return data;
    } catch (error) {
      console.error("실패:", error.response.data);
    }
  }
};

const Newclassroomchat = () => {
  const cookie = new Cookies();
  const token = cookie.get("token");
  const headers = {
    token: token,
  };
  const navigate = useNavigate();
  const goHome = () => {
    window.location.replace("/home");
  };
  const { classid } = useParams();
  const inputRef = useRef(null);
  const [isConceptChat, setIsConceptChat] = useState(0);
  const [chatMessages, setChatMessages] = useState([]);
  const [classConcepts, setClassConcepts] = useState([]);
  const [isConceptEmpty, setIsConceptEmpty] = useState(1);
  const [currentRoom, setCurrentRoom] = useState("default chatroom");

  useCheckLogin();

  const handleDefaultChatroom = async () => {
    setIsConceptChat(0);
    getUserChats(classid, headers)
      .then((data) => {
        setChatMessages([...data]);
        console.log("Successfully loaded chats");
      })
      .catch((err) => {
        console.log(err);
      });
  };

  // Submit 함수
  const handleSubmit = async () => {
    const content = inputRef.current?.value;
    if (inputRef && inputRef.current) {
      inputRef.current.value = "";
    }
    const newMessage = { role: "user", content };
    setChatMessages((prev) => [...prev, newMessage]);
    const chatData = await sendChatRequest(
      isConceptChat,
      classid,
      content,
      headers
    );
    setChatMessages([...chatData]);
  };

  // 리스트의 컨셉 개념 클릭했을 때
  const handleConceptClick = async (concept_id, concept_name) => {
    setIsConceptChat(concept_id);
    setCurrentRoom(concept_name);
    console.log(concept_id);
    console.log(concept_name);
    getConceptChats(classid, headers, concept_id)
      .then((data) => {
        console.log("Successfully loaded CONCEPT chats Dictionary");
        // console.log("######chatData:", JSON.stringify(data, null, 2));
        if (data && Array.isArray(data) && data.length > 0) {
          setChatMessages([...data]);
          setIsConceptEmpty(0);
          console.log("isConceptEmpty: ", isConceptEmpty);
          console.log("######chatData:", JSON.stringify(data, null, 2));
        } else {
          // Clear chat messages if data is empty
          setChatMessages([]);
          setIsConceptEmpty(1);
          console.log("isConceptEmpty: ", isConceptEmpty);
          console.log("No chat data available or data is empty.");
        }
      })
      .catch((err) => {
        console.log(err);
      });
  };

  useLayoutEffect(() => {
    getUserChats(classid, headers)
      .then((data) => {
        setChatMessages([...data]);
        console.log("Successfully loaded chats");
      })
      .catch((err) => {
        console.log(err);
      });

    getClassConcepts(classid, headers)
      .then((data) => {
        setClassConcepts([...data]);
        console.log("Successfully loaded concepts");
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <div className={styles.page}>
      <div className={styles.containerR}>
        <div className={styles.left}>
          <div className={styles.containerC}>
            <div className={styles.lefttop}>
              <div className={styles.ltBack}>
                <h1 className={StylesL.logo_chat} onClick={goHome}>
                  CATCHUP
                </h1>
              </div>
              <div className={styles.ltClassname}>New Classroom</div>
            </div>
            <div className={styles.leftmiddle}>
              <div className={styles.containerC}>
                {chatMessages.map((chat, index) => (
                  <ChatItem
                    content={chat.content}
                    role={chat.role}
                    key={index}
                  />
                ))}
              </div>
            </div>
            <div className={styles.leftbottom}>
              <input
                ref={inputRef}
                type="text"
                placeholder={
                  isConceptChat
                    ? "학습하면서 생기는 궁금한 점을 질문해보세요!"
                    : "어떤 과목을 따라잡고 싶은가요?"
                }
                className={styles.inputBlock}
              />
              <button onClick={handleSubmit} className={styles.button}>
                <IoMdSend />
              </button>
            </div>
          </div>
        </div>
        <div className={styles.right}>
          <div className={styles.containerC}>
            <div className={styles.righttop}>{currentRoom}</div>
            <div className={styles.rightmiddle}>
              <div>
                <div onClick={handleDefaultChatroom}>default chatroom</div>
                {classConcepts.map((concept, index) => (
                  <ConceptItem
                    onClick={handleConceptClick}
                    concept={concept}
                    key={index}
                  ></ConceptItem>
                ))}
              </div>
            </div>
            <div className={styles.rightbottom}>
              <div className={styles.rbIcon} onClick={goHome}>
                <HomeLogo2 className={styles.backIc} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Newclassroomchat;
