let csrftoken = getCookie('csrftoken');

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



let btns = document.getElementsByClassName('addtocart')
for(let i = 0; i < btns.length; i++){
    btns[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        location.reload()
        
        if (user === "AnonymousUser"){
            console.log("User is not logged in")
        }
        else{
            updateCart(productId, action)
        }

    })

}
function updateCart(id, action){
    let url = "/updatecart"
    fetch(url, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({"productId": id, "action": action})
    })
    .then(response => response.json())
    .then(data => console.log(data))
}
let quantityField = document.getElementsByClassName('quantity');

for (let i = 0; i < quantityField.length; i++) {
  quantityField[i].addEventListener('change', function () {
    let quantityFieldValue = quantityField[i].value;
    let quantityFieldProduct = quantityField[i].parentElement.parentElement.children[1].children[0].innerText;
    let url = "/updatequantity";
    fetch(url, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      },
      body: JSON.stringify({ "qfv": quantityFieldValue, "qfp": quantityFieldProduct, })
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        location.reload();
      })
      .catch(error => {
        console.error(error);
        alert("There was an error updating the quantity. Please try again.");
      });
  });
}
