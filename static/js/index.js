if(localStorage.getItem("user")) {
  axios.get("/api/get-posts?user="+localStorage.getItem("user")).then((r) => {
    var resposta = r.data
    resposta.posts.forEach((artigo) => {
      document.querySelector(".list-posts").innerHTML += `
        <div class="post">
        <!-- Infos do usuario -->
        <div class="header-post">
          <i class="fa-brands fa-connectdevelop"></i>
          <strong>@${artigo.author}</strong>
        </div>
        <!-- conteudo -->
        <p id="conteudo">${artigo.text}</p>
        </div>
      </div>
      `
    })
  })
} else {
  axios.get("/api/get-posts?user=visit").then((r) => {
    var resposta = r.data
    resposta.artigos.forEach((artigo) => {
      document.querySelector(".list-posts").innerHTML += `
        <div class="post">
        <!-- Infos do usuario -->
        <div class="header-post">
          <i class="fa-brands fa-connectdevelop"></i>
          <strong>@${artigo.author}</strong>
        </div>
        <!-- conteudo -->
        <p id="conteudo">${artigo.text}</p>
        </div>
      </div>
      `
    })
  })
}

function publicar() {
  if(localStorage.getItem("user")) {
  axios.post("/api/criar-post", {
    "text": document.getElementById("texto").value,
    "author": localStorage.getItem("user")
  }).then((r) => {
    if(r.data.msg === "success") {
      document.querySelector(".list-posts").innerHTML += `
        <div class="post">
        <!-- Infos do usuario -->
        <div class="header-post">
          <i class="fa-brands fa-connectdevelop"></i>
          <strong>@${localStorage.getItem("user")}</strong>
        </div>
        <!-- conteudo -->
        <p id="conteudo">${document.getElementById("texto").value}</p>
        </div>
      </div>
      `
      return alert("Artigo publicado com sucesso!")
    }
  })
  } else {
    alert("Você precisa se cadastrar no site para publicar o post!")
    var pergunta = confirm("Deseja se cadastrar de forma rápida?")
    if(pergunta === true) {
      // cadastro
      var username = prompt("Qual vai ser seu nome de usuário?")
      if(username === false) {
        return alert("Cadastro cancelado com sucesso!")
      }
      if(username === " " || username === "") {
        return alert("Digite alguma coisa!")
      }
      var senha = prompt("Agora digite sua senha! Não esquece dela hein!")
      if(senha === false) {
        return alert("Cadastro cancelado com sucesso!")
      }
      if(senha === " " || senha === "") {
        return alert("Digite alguma coisa!")
      }

      axios.post("/api/cadastrar", {
        "username": username,
        "password": senha
      }).then((res) => {
        var r = res.data 
        if(r.msg === "success") {
          localStorage.setItem("user", username)
          return alert("Conta criada com sucesso! Rápido né?")
        } else {
          return alert("Ocorreu um erro ao criar sua conta! Tente novamente mais tarde!")
        }
      })
    }
  }
}

function clickUser() {
  if(localStorage.getItem("user")) {
    Swal.fire({
      title: "O que você deseja fazer?",
      html: `
        <button onclick="deleteAccount()">Deletar Conta</button>
        <button onclick="changePassword()">Mudar Senha</button>
      `
    })
  }
}

function deleteAccount() {
  var confirme = confirm("Deseja realmente deletar sua conta?")
  if(confirme === true) {
    var senha = prompt("Digite sua senha")
    axios.post("/api/delete-account?user="+localStorage.getItem("user")+"&senha="+senha).then((r) => {
      var resposta = r.data
      if(resposta.msg === "success") {
        localStorage.removeItem("user")
        return alert("Conta Deletada com sucesso!")
      } else {
        return alert("Erro ao deletar sua conta")
      }
    })
  }
}

function changePassword() {
    var confirme = confirm("Deseja realmente mudar a senha?")
  if(confirme === true) {
    var senha = prompt("Digite sua atual senha")
    var senhaNova = prompt("Digite sua nova senha")
    axios.get("/api/change-password?user="+localStorage.getItem("user")+"&senha-atual="+senha+"&senha-nova="+senhaNova).then((r) => {
      var resposta = r.data
      if(resposta.msg === "success") {
        return alert("Senha Editada com sucesso!")
      } else {
        return alert("Erro ao deletar sua conta")
      }
    })
  }
}