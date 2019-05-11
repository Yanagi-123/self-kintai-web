var punchApp = new Vue({
  el: '#table',
  // jinja2のデリミタ {{}} と競合するため、デリミタを変更
  delimiters: ["[[", "]]"],
  data: {
    buttonStr: "修正",
    items: [],
  },
  mounted: function() {
    this.getRecords();
  },
  methods: {
    getRecords: function() {
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
        }
      };
      axios.get('/attendance/get', {
          params: {
            year: 2019,
            month: 5
          }
        })
        .then(response => {
          let attendances = response.data;
          this.items = attendances;

        }).catch(error => {
          console.log(error);
        });
    }
  }
})
