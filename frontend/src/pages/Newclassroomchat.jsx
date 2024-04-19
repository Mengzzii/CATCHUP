// "/new/class/${classid}"
import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
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
    const res = await axios.get("http://127.0.0.1:8000/user/getallchats", {
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
    const res = await axios.get(`http://127.0.0.1:8000/chat/getclassconcepts`, {
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

// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!개념별 chat 가져오는 함수
const getConceptChats = async (classid, headers, concept_id) => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/getconceptchats`, {
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

const sendChatRequest = async (isConceptChat, classid, msg, headers) => {
  console.log(isConceptChat);
  if (isConceptChat) {
    const concept_id = isConceptChat;
    try {
      const res = await axios.post(
        `http://127.0.0.1:8000/chat/concept/qna/${classid}/${msg}/${concept_id}`,
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
        `http://127.0.0.1:8000/chat/new/${classid}/${msg}`,
        null,
        { headers: headers }
      );
      const data = await res.data;
      console.log("Response:", JSON.stringify(data, null, 2));
      window.location.replace(`/class/${classid}`);
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
  // const [refresh, setRefresh] = useState(1);

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

  //Submit 함수
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

  //!!!!!!!!!!!!!!!!!!!!!!!!!
  const handleConceptClick = async (concept_id) => {
    setIsConceptChat(concept_id);
    console.log(concept_id);
    getConceptChats(classid, headers, concept_id)
      .then((data) => {
        console.log("Successfully loaded CONCEPT chats DIctionary");
        console.log("######chatData:", JSON.stringify(data, null, 2));
        if (data && Array.isArray(data) && data.length > 0) {
          setChatMessages([...data]);
          console.log("######chatData:", JSON.stringify(data, null, 2));
        } else {
          // Clear chat messages if data is empty
          setChatMessages([]);
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

  // useEffect(() => {
  //   getClassConcepts(classid, headers)
  //     .then((data) => {
  //       setClassConcepts([...data]);
  //       console.log("Successfully loaded concepts");
  //     })
  //     .catch((err) => {
  //       console.log(err);
  //     });
  //   classConcepts.map((concept, index) => (
  //     <ConceptItem
  //       onClick={handleConceptClick}
  //       concept={concept}
  //       key={index}
  //     ></ConceptItem>
  //   ));
  // }, [refresh]);

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
            <div className={styles.righttop}>현재 개념</div>
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
