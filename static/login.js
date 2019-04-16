var loginApp = new Vue({
  el: '#loginApp',
  // jinja2のデリミタ {{}} と競合するため、デリミタを変更
  delimiters: ["[[", "]]"],
  data: {
    userId: "",
    password: "",
    userIdError: "",
    passwordError: ""
  },
  methods: {
    validateUserId: function() {
      if (this.userId === "") {
        this.userIdError = "ユーザIDを入力してください。";
      }
      if (!this.userId.match(/^([0-9]|[a-z]|[A-Z]|_|-)+$/g)) {
        this.userIdError = "ユーザIDに使用できない文字が入力されています。";
      }
    },
    validatePassword: function() {
      if (this.passwordError === "") {
        this.passwordError = "ユーザIDを入力してください。";
      }
      if (!this.password.match(/^([0-9]|[a-z]|[A-Z]|_|-)+$/g)) {
        this.userIdError = "パスワードに使用できない文字が入力されています。";
      }
    }
  }
})
