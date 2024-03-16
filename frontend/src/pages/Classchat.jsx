import React, { useEffect, useLayoutEffect, useRef, useState }  from 'react';
import ChatItem from "../components/ChatItem";
import ConceptItem from "../components/ConceptItem";
import axios from 'axios';
import { IoMdSend } from "react-icons/io";

const getUserChats = async (id, classroom_id) => {
    try {
      const res = await axios.get(`http://127.0.0.1:8000/sample/getallchats/${id}/${classroom_id}`);
        if (res.status !== 200) {
        throw new Error("Unable to send chat");
  }
  console.log("get User Chats / Response:", JSON.stringify(res, null, 2));
  const data = await res.data;
  return data;} 
    catch (error) {
      console.error("실패:", error.response.data.detail[0]);
    }
  
};

const getConceptChats = async (id, classroom_id, concept_id) => {
    try {
      const res = await axios.get(`http://127.0.0.1:8000/getconceptchats/${id}/${classroom_id}/${concept_id}`);
        if (res.status !== 200) {
        throw new Error("Unable to send chat");
  }
  console.log("get Concept Chats / Response:", JSON.stringify(res, null, 2));
  const data = await res.data;
  return data;} 
    catch (error) {
      console.error("실패:", error.response.data.detail[0]);
    }
  
};

const getClassConcepts = async (id, classroom_id) => {
    try {
      const res = await axios.get(`http://127.0.0.1:8000/getclassconcepts/${id}/${classroom_id}`);
        if (res.status !== 200) {
        throw new Error("Unable to send chat");
  }
  console.log("Response:", JSON.stringify(res, null, 2));
  const data = await res.data;
  return data;} 
    catch (error) {
      console.error("실패:", error.response.data.detail[0]);
    }
  
};

const sendChatRequest = async (user_id, classroom_id, message) => {
    try {
        const res = await axios.post(`http://127.0.0.1:8000/chat/new/${user_id}/${classroom_id}/${message}`);
        console.log("Response:", JSON.stringify(res, null, 2));
        const data = await res.data;
          return data;
    }
    
    catch (error) {
      console.error("실패:", error.response.data);
    }
}



const Classchat = () => {
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
      const user_id = 'hello';
      const classroom_id = '2df997c3-5ec6-4482-9de6-430c2eb22c96';
      const chatData = await sendChatRequest(user_id, classroom_id, content);
      
      setChatMessages([...chatData]);
  };

    const handleConceptClick= async ()=>{
      const id = 'hello';
      const classroom_id = '2df997c3-5ec6-4482-9de6-430c2eb22c96';
      const concept_id = '6cc79398-b5b0-4576-8e0c-02f2a951b0b5';
      getConceptChats(id, classroom_id, concept_id)
        .then((data) => {
          console.log("Successfully loaded CONCEPT chats");
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
      const id = 'hello';
      const classroom_id = '2df997c3-5ec6-4482-9de6-430c2eb22c96';
      getUserChats(id, classroom_id)
        .then((data) => {
          setChatMessages([...data]);
          console.log("Successfully loaded chats");
        })
        .catch((err) => {
          console.log(err);
        });

      getClassConcepts(id, classroom_id)
        .then((data) => {
          setClassConcepts([...data]);
          console.log("Successfully loaded concepts");
        })
        .catch((err) => {
          console.log(err);
        });




  }, []);


    return (

        <div style={{//background
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
        }}> 

            <div style = {{ //divied into <L> column section
            display: "flex",
            flex: 0.8,
            flexDirection: "column",
            paddingLeft: "3px",
            paddingRight:"3px",
            backgroundColor:"#767676"}}>

                <div style={{ //Chat section
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
                scrollBehavior: "smooth",}}>

                    {chatMessages.map((chat, index) => (
            <ChatItem content={chat.content} role={chat.role} key={index} />
          ))}

                </div>

                <div style={{ //User Input section; Input bar
                width: "100%",
                borderRadius: "8px",
                backgroundColor: "#FFA6A6",
                display: "flex",
                margin: "auto"}}>

                    
                    <input ref={inputRef} 
                    type="text"    style={{ //Input block
                    width: "100%",
                    backgroundColor: "transparent",
                    padding: "30px",
                    border: "none",
                    outline: "none",
                    color: "white",
                    fontSize: "20px"}}/>

                    <button onClick={handleSubmit} style={{ color: 'white', margin: '0 0.5rem' }}>
                      <IoMdSend />
                    </button>
                    
                </div>


            </div>

            <div style={{ //divied into <R> column section 
            display: "flex",
            flex: 0.2, 
            backgroundColor: "#FFFFFF",
            flexDirection: "column"}}>
                
                <div style={{
                display: "flex",
                width: "100%",
                height: "60vh",
                backgroundColor: "#FFFFFF",
                border: "1px solid #ccc",
                borderRadius: "5px",
                flexDirection: "column",
                marginLeft: "3px",
                marginRight: "3px"
                }}> hello?

                {classConcepts.map((concept, index)=>
                (<ConceptItem onClick={handleConceptClick} concept = {concept} key={index}></ConceptItem>))
                }
                </div>

            </div>

        </div>
    )
};

export default Classchat