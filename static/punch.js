var punchApp = new Vue({
  el: '#punchApp',
  // jinja2のデリミタ {{}} と競合するため、デリミタを変更
  delimiters: ["[[", "]]"],
  data: {
    clock: "",
  },
  methods: {
    aaa: function() {
      console.log("aaa");
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          "Access-Control-Allow-Origin": "*",
        }
      };
      axios.post('/punch', JSON.stringify({
          clock: this.clock
        }), axiosConfig)
        .then(response => {
          console.log(response.data);
          console.log('送信したテキスト: ' + response);
        }).catch(error => {
          console.log(error);
        });
    }
  }
})
