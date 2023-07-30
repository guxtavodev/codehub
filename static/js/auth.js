function cadastrar() {
  if(localStorage.getItem("user")) {
    Swal.fire("Ei! Perai!", "Você já uma conta neste dispositivo, não precisa criar outra.", "warning")
    window.location.href = "/"
  }

  var username = document.querySelector("#username").value 
  var senha = document.querySelector("#password").value

  axios.post("/api/cadastrar", {
        "username": username,
        "password": senha
      }).then((res) => {
        var r = res.data 
        if(r.msg === "success") {
          localStorage.setItem("user", username)
          localStorage.setItem("primeira-vez", "sim")
          window.location.href = "/"
        } else {
          return Swal.fire("Erro", "Ocorreu um erro ao criar a sua conta, tente novamente mais tarde", "error")
        }
      })
}

function entrar() {
  if(localStorage.getItem("user")) {
    Swal.fire("Ei! Perai!", "Você já uma conta neste dispositivo, não precisa se autenticar", "warning")
    window.location.href = "/"
  }

  var username = document.querySelector("#username").value 
  var senha = document.querySelector("#password").value

  axios.get("/api/auth?username="+username+"&password="+senha).then((res) => {
    var msg = res.data
    if(msg.msg === "success") {
      localStorage.setItem("user", username)
      window.location.href = "/"
    } else if(msg.msg === "incorrect password") {
      return Swal.fire("Não Autorizado", "Senha incorreta!", "error")
    } else {
      return Swal.fire("Erro ao se conectar", "", "error")
    }
  })
}
