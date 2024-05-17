// 로그인된 상태인지 확인한다:
// : 쿠키에 token/name 정보 없을 시 기본 홈화면으로 이동
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Cookies } from "react-cookie";

const useCheckLogin = () => {
  const navigate = useNavigate();
  const cookie = new Cookies();

  useEffect(() => {
    const userName = cookie.get("name");
    const userToken = cookie.get("token");

    if (userName === undefined) {
      console.log("login: false");
      navigate("/");
    }
  }, []);
};

export default useCheckLogin;
