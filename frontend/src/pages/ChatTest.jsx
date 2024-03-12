// 링크는 "/chat/:classid"
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { Cookies } from "react-cookie";

const ChatTest = () => {
  const cookie = new Cookies();
  const { classid } = useParams();

  return <div>{classid}</div>;
};

export default ChatTest;
