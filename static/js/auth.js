function cadastrar() {
  if (localStorage.getItem("user")) {
    Swal.fire("Ei! Perai!", "Você já tem uma conta neste dispositivo, não precisa criar outra.", "warning");
    window.location.href = "/";
    return;
  }

  var username = document.querySelector("#username").value;
  var senha = document.querySelector("#password").value;

  // Verificar se a senha não está vazia
  if (!senha.trim()) {
    return Swal.fire("Erro", "A senha não pode estar vazia.", "error");
  }

  // Remover caracteres indesejados do nome de usuário e verificar se contém pelo menos uma letra
  var cleanedUsername = username.replace(/[^a-zA-Z]/g, "");
  if (!cleanedUsername) {
    return Swal.fire("Erro", "O nome de usuário deve conter pelo menos uma letra.", "error");
  }

  // Verificar se o nome de usuário não está vazio após remover caracteres indesejados
  if (!username.trim()) {
    return Swal.fire("Erro", "O nome de usuário não pode estar vazio.", "error");
  }

  axios
    .post("/api/cadastrar", {
      "username": username,
      "password": senha,
    })
    .then((res) => {
      var r = res.data;
      if (r.msg === "success") {
        localStorage.setItem("user", username);
        localStorage.setItem("primeira-vez", "sim");
        window.location.href = "/";
      } else {
        return Swal.fire("Erro", "Ocorreu um erro ao criar a sua conta, tente novamente mais tarde", "error");
      }
    });
}


// Variáveis globais para controle das tentativas e do temporizador
var attempts = 0;
var blocked = false;

function entrar() {
  if (localStorage.getItem("user")) {
    Swal.fire("Ei! Perai!", "Você já tem uma conta neste dispositivo, não precisa se autenticar", "warning");
    window.location.href = "/";
    return;
  }

  var username = document.querySelector("#username").value;
  var senha = document.querySelector("#password").value;

  // Verificar se algum campo está vazio
  if (!username.trim() || !senha.trim()) {
    return Swal.fire("Erro", "Por favor, preencha todos os campos.", "error");
  }

  // Verificar se está bloqueado
  if (blocked) {
    return Swal.fire("Tentativas esgotadas", "Tente novamente em 10 minutos.", "warning");
  }

  axios
    .get("/api/auth?username=" + username + "&password=" + senha)
    .then((res) => {
      var msg = res.data;
      if (msg.msg === "success") {
        localStorage.setItem("user", username);
        window.location.href = "/";
      } else if (msg.msg === "incorrect password") {
        attempts++;

        if (attempts >= 4) {
          // Bloquear por 10 minutos após 4 tentativas falhas
          blocked = true;
          setTimeout(() => {
            blocked = false;
            attempts = 0;
          }, 600000); // 10 minutos em milissegundos
        }

        return Swal.fire("Não Autorizado", "Senha incorreta! Tentativas restantes: " + (4 - attempts), "error");
      } else {
        return Swal.fire("Erro ao se conectar", "", "error");
      }
    })
    .catch((err) => {
      return Swal.fire("Erro ao se conectar", "", "error");
    });
}
