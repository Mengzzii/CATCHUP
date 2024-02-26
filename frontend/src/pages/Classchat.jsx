import React, { useEffect, useLayoutEffect, useRef, useState }  from 'react'
import ChatItem from "../components/ChatItem";
import axios from 'axios';

const getUserChats = async (id) => {
    try {const res = await axios.get("http://127.0.0.1:8000/sample/getallchats/{id}");
if (res.status !== 200) {
    throw new Error("Unable to send chat");
  }
  const data = await res.data;
  return data;} 
    catch (error) {
      console.error("실패:", error.response.data.detail[0]);
    }
  

};


const Classchat = () => {
    const [chatMessages, setChatMessages] = useState([]);

    useLayoutEffect(() => {
      const id = 'hello';
      getUserChats(id)
        .then((data) => {
        console.log(data+"!!!!!!!!!!!!!");
          setChatMessages([...data]);
          console.log(chatMessages+"@@@@@@@@@@@@@@@@@@@@@@@@@@@@");
          console.log("Successfully loaded chats");
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
                backgroundColor: "#767676",
                display: "flex",
                margin: "auto"}}>

                    
                    <input type="text"    style={{ //Input block
                    width: "100%",
                    backgroundColor: "transparent",
                    padding: "30px",
                    border: "none",
                    outline: "none",
                    color: "white",
                    fontSize: "20px"}}/>
                    
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

                {/*chatRooms.map()*/ }
                </div>

            </div>

        </div>
    )
};

export default Classchat