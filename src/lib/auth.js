import { get, post } from "@/lib/http";

const isAuthkeyALive = async (authkey) => {
  //   await post("/api/user/info", { authkey: authkey }).then((res) => {
  //     if (res.code == 200) {
  //       return res.data;
  //     } else {
  //       return undefined;
  //     }
  //   });
  return post("/api/user/info", { authkey: authkey });
  if (test.data.code == 200) {
    return test.data;
  }
  return undefined;
};

export { isAuthkeyALive };
