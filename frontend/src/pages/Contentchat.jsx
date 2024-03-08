import { Link, useNavigate } from "react-router-dom";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Cookies } from "react-cookie";
import getUserId from "../components/Auth.jsx";

const Contentchat = () => {
  {
    getUserId();
  }
  return (
    <>
      <div>개념챗방</div>
    </>
  );
};

export default Contentchat;
