// 컨셉챗
import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import ChatItem from "../components/ChatItem";
import ConceptItem from "../components/ConceptItem";
import axios from "axios";
import { IoMdSend } from "react-icons/io";
import { Cookies } from "react-cookie";
import { useParams } from "react-router-dom";

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

// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!개념별 chat 가져오는 함수
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

const sendChatRequest = async (isConceptChat, classid, msg, headers) => {
  if (isConceptChat) {
    const concept_id = isConceptChat;
    try {
      const res = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/chat/concept/new/${classid}/${msg}/${concept_id}`,
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
      return data;
    } catch (error) {
      console.error("실패:", error.response.data);
    }
  }
};

const Classroomchat = () => {
  const cookie = new Cookies();
  const token = cookie.get("token");
  const headers = {
    token: token,
  };
  const { classid } = useParams();
  const inputRef = useRef(null);
  const [isConceptChat, setIsConceptChat] = useState(0);
  const [chatMessages, setChatMessages] = useState([]);
  const [classConcepts, setClassConcepts] = useState([]);

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

  return (
    <div
      style={{
        //background
        display: "flex",
        flex: 1,
        width: "100%",
        height: "100%",
        marginTop: "1rem",
        gap: "1rem",
        border: "1px solid #ccc",
        padding: "1rem",
        backgroundColor: "#f0f0f0",
        borderRadius: "5px",
      }}
    >
      <div
        style={{
          //divied into <L> column section
          display: "flex",
          flex: 0.8,
          flexDirection: "column",
          paddingLeft: "3px",
          paddingRight: "3px",
          backgroundColor: "#767676",
        }}
      >
        <div
          style={{
            //Chat section
            width: "100%",
            height: "60vh",
            borderRadius: "3px",
            marginLeft: "auto",
            marginRight: "auto",
            display: "flex",
            flexDirection: "column",
            overflow: "scroll",
            overflowX: "hidden",
            overflowY: "auto",
            scrollBehavior: "smooth",
          }}
        >
          {chatMessages.map((chat, index) => (
            <ChatItem content={chat.content} role={chat.role} key={index} />
          ))}
        </div>

        <div
          style={{
            //User Input section; Input bar
            width: "100%",
            borderRadius: "8px",
            backgroundColor: "#FFA6A6",
            display: "flex",
            margin: "auto",
          }}
        >
          <input
            ref={inputRef}
            type="text"
            style={{
              //Input block
              width: "100%",
              backgroundColor: "transparent",
              padding: "30px",
              border: "none",
              outline: "none",
              color: "white",
              fontSize: "20px",
            }}
          />

          <button
            onClick={handleSubmit}
            style={{ color: "white", margin: "0 0.5rem" }}
          >
            <IoMdSend />
          </button>
        </div>
      </div>

      <div
        style={{
          //divied into <R> column section
          display: "flex",
          flex: 0.2,
          backgroundColor: "#FFFFFF",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            display: "flex",
            width: "100%",
            height: "60vh",
            backgroundColor: "#FFFFFF",
            border: "1px solid #ccc",
            borderRadius: "5px",
            flexDirection: "column",
            marginLeft: "3px",
            marginRight: "3px",
          }}
        >
          <button onClick={handleDefaultChatroom}>default chatroom</button>

          {classConcepts.map((concept, index) => (
            <ConceptItem
              onClick={handleConceptClick}
              concept={concept}
              key={index}
            ></ConceptItem>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Classroomchat;
