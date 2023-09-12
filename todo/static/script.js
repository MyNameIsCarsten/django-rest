// Acquiring the csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Example of fetching data from our api using async function
async function fetchData() {
    try {
      // Send a GET request to the specified URL with headers
      // Wait until we get a response from fetch
      const response = await fetch("/todos/api/1/", {
        method: "get",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token in headers
          "Accept": "application/json", // Specify that we want JSON response
          "Content-Type": "application/json", // Specify JSON as content type
        },
      });
  
      // Check if the response status is not OK (e.g., 404 or 500)
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      // Parse the JSON response body:
      // response.json() method is another asynchronous operation
      // we pause the execution of fetchData until the Promise returned by response.json() is resolved
      const data = await response.json();
  
      // Log the retrieved data to the console
      console.log("Data is ok", data);
    } catch (ex) {
      // Handle any errors that occur during the fetch or parsing
      console.log("Fetching data failed", ex);
    }
  }
  
  // Call the async function to fetch data
  fetchData();
