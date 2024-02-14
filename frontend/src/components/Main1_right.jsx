import React from "react";
import Login_button from "../components/Login_button";
import Signup_bt from "../components/Signup_bt";
import { Link } from "react-router-dom";

const Main1_right = () => {
  return (
    <div>
      <div>시작하기</div>
      <Link to="/signup">
        <Signup_bt />
      </Link>
      <Link to="/login">
        <Login_button />
      </Link>
    </div>
  );
};

export default Main1_right;
