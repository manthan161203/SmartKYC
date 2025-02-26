export const getAccessToken = () => {
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("access_token="));
  
  return cookie ? cookie.split("=")[1] : null;
};