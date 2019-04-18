var registerApp = new Vue({
  el: '#registerApp',
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
      if (!this.userId.match(/^([0-9]|[a-z]|[A-Z]|_|-){4,20}$/g)) {
        this.userIdError = "ユーザIDには、半角英数字(a~z, 0~9)及び、記号のハイフン(-)、アンダースコア(_)を4文字以上、20文字以下組み合わせた文字列を入力してください。";
      }
    },
    validatePassword: function() {
      if (!this.password.match(/^([0-9]|[a-z]|[A-Z]|_|-){4,20}$/g)) {
        this.passwordError = "パスワードには、半角英数字(a~z, 0~9)及び、記号のハイフン(-)、アンダースコア(_)を4文字以上、20文字以下組み合わせた文字列を入力してください。";
      }
    }
  }
})
