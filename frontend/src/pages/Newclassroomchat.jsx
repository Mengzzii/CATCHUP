import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import ChatItem from "../components/ChatItem";
import axios from "axios";
import { IoMdSend } from "react-icons/io";
import { Cookies } from "react-cookie";
import { useParams } from "react-router-dom";

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
    console.log("Response:", JSON.stringify(res.data, null, 2));
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

const sendChatRequest = async (classid, msg, headers) => {
  try {
    console.log(classid);
    console.log(msg);
    console.log(headers);
    const res = await axios.post(
      `http://127.0.0.1:8000/chat/new/${classid}/${msg}`,
      null,
      { headers: headers }
    );
    console.log("Response:", JSON.stringify(res, null, 2));
    const data = await res.data;
    return data;
  } catch (error) {
    console.error("실패:", error.response.data);
  }
};

const Newclassroomchat = () => {
  const cookie = new Cookies();
  const token = cookie.get("token");
  const headers = {
    token: token,
  };
  const { classid } = useParams();
  const inputRef = useRef(null);
  const [chatMessages, setChatMessages] = useState([]);
  const [classConcepts, setClassConcepts] = useState([]);
  const handleSubmit = async () => {
    const content = inputRef.current?.value;
    if (inputRef && inputRef.current) {
      inputRef.current.value = "";
    }
    const newMessage = { role: "user", content };
    setChatMessages((prev) => [...prev, newMessage]);
    const chatData = await sendChatRequest(classid, content, headers);
    // console.log("######chatData:", JSON.stringify(chatData, null, 2));
    setChatMessages([...chatData]);
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
          {" "}
          hello?
          {/* {classConcepts.map((concept, index)=>
                (<ConceptItem concept = {concept} key={index}></ConceptItem>))
                  
                } */}
        </div>
      </div>
    </div>
  );
};

export default Newclassroomchat;
