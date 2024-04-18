import React from "react";
import { Cookies } from "react-cookie";
import TomatoIcon from "../components/TomatoIcon";
import UserIcon from "../components/UserIcon";

const ChatItem = ({ content, role }) => {
  const cookie = new Cookies();
  const messageBlocks = [content];

  return role == "assistant" ? (
    <div>
      <div style={{ fontWeight: "Bold" }}>
        <TomatoIcon />
        &nbsp; CATCHUP
      </div>
      {/* {!messageBlocks && (
                <Typography sx={{ fontSize: "20px" }}>{content}</Typography>
                 )} */}
      {messageBlocks &&
        messageBlocks.length &&
        messageBlocks.map((block) => (
          <div style={{ fontSize: "17px" }}>{block}</div>
        ))}
      <br />
    </div>
  ) : (
    <div>
      <div style={{ fontWeight: "Bold" }}>
        <UserIcon />
        &nbsp;&nbsp;{cookie.get("name")}
      </div>
      <div>
        {/* {!messageBlocks && (
                <Typography sx={{ fontSize: "20px" }}>{content}</Typography>
                 )} */}
        {messageBlocks &&
          messageBlocks.length &&
          messageBlocks.map((block) => (
            <div style={{ fontSize: "17px" }}>{block}</div>
          ))}
        <br />
      </div>
    </div>
  );
};

export default ChatItem;
