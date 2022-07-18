const inputField = document.getElementById("input");
inputField.addEventListener("keydown", (e) => {
  if (e.code === "Enter") {
    let input = inputField.value;
    inputField.value = "";

    const messagesContainer = document.getElementById("messages");
    let userDiv = document.createElement("div");
    userDiv.id = "user";
    userDiv.className = "user response";
    userDiv.innerHTML = `<span><b>Me: </b> ${input}</span>`;
    messagesContainer.appendChild(userDiv);
  
    let botDiv = document.createElement("div");
    let botText = document.createElement("span");
    botDiv.id = "bot";
    botDiv.className = "bot response";
    botText.innerText = "Typing...";

    botDiv.appendChild(botText);
    messagesContainer.appendChild(botDiv);
  
    messagesContainer.scrollTop =
      messagesContainer.scrollHeight - messagesContainer.clientHeight;

    output(input, botText);
  }
});

function output(input, botText) {
  let product;
  let text = input

  product= get_product(input)

  addChatEntry(input, product, botText);
}

function compare(utterancesArray, answersArray, string) {
  let reply;
  let replyFound = false;
  for (let x = 0; x < utterancesArray.length; x++) {
    for (let y = 0; y < utterancesArray[x].length; y++) {
      if (utterancesArray[x][y] === string) {
        let replies = answersArray[x];
        reply = replies[Math.floor(Math.random() * replies.length)];
        replyFound = true;
        break;
      }
    }
    if (replyFound) {
      break;
    }
  }
  return reply;
}

function addChatEntry(input, product,botText) {



  //setTimeout(() => {
    botText.innerHTML = '<b>HelperBot: </b>' 
    botText.innerHTML += `${product}`;
 // }, 700);
}



function get_product(input){


    return $.get_product_data(input)


}


jQuery.extend({
  get_product_data: function(input ) {
      var result = null;
      $.ajax({
          type: 'GET',
          url: '/chatbot-response/',
          dataType: 'json',
          data: { 'input':input },
        
          async: false,
          success: function(response) {
            result= response['text']
            console.log(result)
          },
          error: function(error){
            console.log(error)
           }

      });
     return  result;
  }
});

