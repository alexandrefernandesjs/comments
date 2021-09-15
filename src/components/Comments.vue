<template>
  <div class="container">
    <h1>Comentários</h1>
    <hr />
    <Form v-on:add-todo="addComment"></Form>
    <div class="list-group">
      <p v-if="comments.length <= 0">Sem comentários...</p>
      <div
        v-else
        class="list-group-item"
        v-for="(comment, index) in allComments"
        v-bind:key="index"
      >
        <span class="comment__author"
          >Autor: <strong>{{ comment.nome }}</strong></span
        >
        <p>{{ comment.mensagem }}</p>
        <div>
          <svg
            style="margin-right: 4%"
            v-on:click.prevent="removeComment(index)"
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            fill="currentColor"
            class="bi bi-trash"
            viewBox="0 0 16 16"
          >
            <path
              d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"
            />
            <path
              fill-rule="evenodd"
              d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
            />
          </svg>

          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            fill="currentColor"
            class="bi bi-pen"
            viewBox="0 0 16 16"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
            @click="editComment(index)"
          >
            <path
              d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001zm-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708l-1.585-1.585z"
            />
          </svg>
        </div>
      </div>
    </div>

    <div class="modal" tabindex="-1" id="exampleModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Editar comentario</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <p>
              <input
                placeholder="nome"
                type="text"
                name="author"
                class="form-control"
                v-model="editName"
              />
            </p>
            <p>
              <textarea
                placeholder="Comentário"
                name="message"
                class="form-control"
                v-model="editMessage"
              ></textarea>
            </p>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-danger"
              data-bs-dismiss="modal"
            >
              Fechar
            </button>
            <button
              type="button"
              class="btn btn-primary"
              @click="edit()"
              data-bs-dismiss="modal"
            >
              Salvar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Form from "./Form";
import axios from "axios";

export default {
  components: {
    Form,
  },
  data() {
    return {
      comments: [],
      editName: "",
      editMessage: "",
      t_id: "",
      t_name: "",
      t_message: "",
    };
  },
  mounted() {
    axios
      .get("http://127.0.0.1:5000/comments")
      .then((response) => (this.comments = response.data));
  },
  methods: {
    addComment(comment) {
      this.comments.push(comment);
    },
    removeComment(index) {
      axios
        .delete("http://127.0.0.1:5000/comments/" + this.comments[index].id, {})
        .then(function (response) {
          console.log(response.data);
        })
        .catch(function (error) {
          console.log(error);
        });
      this.comments.splice(index, 1);
    },
    editComment(index) {
      this.t_index = index;
      this.t_id = this.comments[index].id;
      this.t_name = this.comments[index].nome;
      this.t_message = this.comments[index].mensagem;
    },
    edit() {
      axios
        .put("http://127.0.0.1:5000/comments/" + this.t_id, {
          id: this.t_id,
          nome: this.editName,
          mensagem: this.editMessage,
        })
        .then(function (response) {
          var statusCode = response.status;

          if (statusCode == "200") {
            console.log("Atualizado com sucesso");
          }
        })
        .catch(function (error) {
          console.log(error);
        });
      this.comments[this.t_index].nome = this.editName;
      this.comments[this.t_index].mensagem = this.editName;
      this.editName = "";
      this.editMessage = "";
    },
  },
  computed: {
    allComments() {
      return this.comments.map((comment) => ({
        ...comment,
        nome: comment.nome.trim() === "" ? "Anônimo" : comment.nome,
      }));
    },
  },
  watch: {
    comments(val) {
      console.log("val", val);
    },
  },
};
</script>