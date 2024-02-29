import React from "react"

const ChatItem = ({content, role}) => {

    const messageBlocks = [content];

    return role == "assistant"? (
        <div style={{
        display: "flex",
        px: "2",
        backgroundColor: "#FB6D6D",
        gap: "2",
        borderRadius: "2",
        marginTop: "1"}}
    >
            <div>
                <img />
            </div>

            <div>
                {/* {!messageBlocks && (
                <Typography sx={{ fontSize: "20px" }}>{content}</Typography>
                 )} */}
            {messageBlocks &&
              messageBlocks.length &&
              messageBlocks.map((block) =>
            
              <div style={{ fontSize: "20px" }}>{block}</div>

          )}
            </div>

        </div> 
    ) : (
        <div style={{
        display: "flex",
        px: "2",
        backgroundColor: "#D9D9D9",
        gap: "2",
        borderRadius: "2",
        marginTop: "1"}}
    >
            <div>
                <img />
            </div>

            <div>
                {/* {!messageBlocks && (
                <Typography sx={{ fontSize: "20px" }}>{content}</Typography>
                 )} */}
            {messageBlocks &&
              messageBlocks.length &&
              messageBlocks.map((block) =>
            
              <div style={{ fontSize: "20px" }}>{block}</div>

          )}
            </div>
            
        </div> 
    )
}

export default ChatItem;