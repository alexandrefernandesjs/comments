<template>
  <div class="form-todo form-group">
    <p>
      <input
        placeholder="nome"
        type="text"
        name="author"
        class="form-control"
        v-model="nome"
      />
    </p>
    <p>
      <textarea
        placeholder="Comentário"
        name="message"
        class="form-control"
        v-model="mensagem"
      ></textarea>
    </p>
    <button v-on:click="addComment" type="submit" class="btn btn-primary">
      Comentar
    </button>
    <hr />
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      nome: "",
      mensagem: "",
    };
  },
  methods: {
    addComment() {
      if (this.mensagem.trim() === "") {
        return;
      }

      axios
        .post("http://127.0.0.1:5000/comments", {
          nome: this.nome,
          mensagem: this.mensagem,
        })
        .then(function (response) {
          console.log(response.status);
          var statusCode = response.status;

          if (statusCode == "200") {
            console.log("Inserido");
          }
        })
        .catch(function (error) {
          console.log(error);
        });

      this.$emit("add-todo", {
        nome: this.nome,
        mensagem: this.mensagem,
      });
      this.nome = "";
      this.mensagem = "";
    },
  },
};
</script>