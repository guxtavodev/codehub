var posts = document.querySelectorAll(".post")
var userLogado = localStorage.getItem("user")

posts.forEach((div) => {
  var authorPost = div.getAttribute("data-author")
  console.log(authorPost)

  if(authorPost === userLogado) {
    console.log("passou aqui")
    div.innerHTML += `<i onclick="deletePost('${div.getAttribute("data-id")}')" class="fa-solid fa-trash"></i>`
    console.log("ok")
  }
})

function deletePost(post) {
  var senha = prompt("Digite sua senha")
  axios.get("/api/delete-post?post="+post+"&password="+senha).then((res) => {
    var r = res.data 
    if(r.msg === "success") {
      return Swal.fire("Post excluído com sucesso!", "", "success")
    } else {
      return Swal.fire("Erro ao excluir o post", "Tente novamente mais tarde", "error")
    }
  })
}
