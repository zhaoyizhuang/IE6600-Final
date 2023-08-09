import axios from "axios";
import Cookies from "js-cookie";
import Config from "./config";

const isProduction = Config.NODE_ENV === "production";

export default axios.create({
  baseURL: isProduction ? Config.BACKEND_URL : "http://127.0.0.1:8000",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": Cookies.get("csrftoken"),
  },
});
