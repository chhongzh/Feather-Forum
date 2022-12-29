import apiRoute from "@/config/apiRoute";
import { post } from "./http";

const getPost = (id, authkey) => {
  return post(apiRoute.api_post_read, {
    authkey: authkey,
    pid: id,
  });
};

export { getPost };
