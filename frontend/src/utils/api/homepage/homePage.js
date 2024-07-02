/* eslint-disable no-undef */
export async function getHomePage() {
  const url = `${process.env.REACT_APP_API_LINK}api/homepage`
  // const response = await fetch(
  //   process.env.REACT_APP_API_LINK + "/api/homepage"
  // );
  
  console.log("URL *******")
  console.log(url);
  const response = await fetch(url);
  console.log("Response *******")
  console.log(response);
  if (!response.ok) {
    // alert('failed');
    console.log("response");
    console.log(response);
    throw { message: "Failed to fetch homepage", status: 500 };
  }
  // alert('Success');
  console.log("jsonData");
  console.log(response);
  const jsonData = await response.json();
  
  return jsonData;
}
