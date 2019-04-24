var punchApp = new Vue({
  el: '#punchApp',
  // jinja2のデリミタ {{}} と競合するため、デリミタを変更
  delimiters: ["[[", "]]"],
  data: {
    clock: ""
  },
  mounted: function() {
    setInterval(
      this.bbb, 1000)
  },
  methods: {
    aaa: function() {
      let axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
        }
      };
      var punchInFlag = document.getElementById('punchInFlag').textContent;
      axios.post('/punch', JSON.stringify({
          punching_time: this.clock,
          punch_in_flag: punchInFlag

        }), axiosConfig)
        .then(response => {
          console.log(response.data);
        }).catch(error => {
          console.log(error);
        });
    },
    bbb: function() {
      let date = new Date();
      let year = date.getFullYear().toString();
      let month = (date.getMonth() + 1).toString().padStart(2, "0");
      let day = date.getDate().toString().padStart(2, "0");
      let hour = date.getHours().toString().padStart(2, "0");
      let time = date.getSeconds().toString().padStart(2, "0");
      let minutes = date.getMinutes().toString().padStart(2, "0");
      let seconds = date.getSeconds().toString().padStart(2, "0");
      console.log(year + "/" + month + "/" + day + " " + hour + ":" + minutes + ":" + seconds);
      this.clock = year + "/" + month + "/" + day + " " + hour + ":" + minutes + ":" + seconds;

    }
  }
})
